const { Anthropic } = require('@anthropic-ai/sdk');
const { spawn } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');

// Load environment variables if they exist (e.g., ANTHROPIC_API_KEY)
require('dotenv').config();

// ─── Configuration ────────────────────────────────────────────
const PKG_VERSION = require('../package.json').version;
const DEFAULT_MODEL = 'claude-3-5-sonnet-latest';
const AGENT_MODEL = process.env.AGENT_KIT_MODEL || DEFAULT_MODEL;
const SPAWN_TIMEOUT_MS = 30_000;

const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY || ''
});

// ─── Action Logger ────────────────────────────────────────────
const ACTION_LOG_PATH = path.join(__dirname, '..', '.agent-os', 'logs', 'agent-actions.json');

async function logAction(agentId, toolName, input, result) {
    try {
        let log = { version: '1.0.0', description: 'Audit trail for all agent actions', actions: [] };
        if (await fs.pathExists(ACTION_LOG_PATH)) {
            log = await fs.readJson(ACTION_LOG_PATH);
        }
        log.actions.push({
            timestamp: new Date().toISOString(),
            agent: agentId,
            tool: toolName,
            input: typeof input === 'string' ? input.substring(0, 200) : JSON.stringify(input).substring(0, 200),
            result: typeof result === 'string' ? result.substring(0, 200) : 'ok',
        });
        // Keep last 500 actions max
        if (log.actions.length > 500) log.actions = log.actions.slice(-500);
        await fs.writeJson(ACTION_LOG_PATH, log, { spaces: 2 });
    } catch {
        // Non-critical — don't crash the engine for logging failures
    }
}

// ─── Agent Prompt Generator ───────────────────────────────────
async function getAgentPrompt(agentId) {
    return new Promise((resolve, reject) => {
        const sourceDir = path.join(__dirname, '..');
        const scriptPath = path.join(sourceDir, 'scripts', 'spawn_agent.py');

        const child = spawn('python', [scriptPath, agentId]);

        let stdout = '';
        let stderr = '';
        let killed = false;

        const timer = setTimeout(() => {
            killed = true;
            child.kill('SIGTERM');
            reject(new Error(`Agent spawn timed out after ${SPAWN_TIMEOUT_MS / 1000}s for ${agentId}`));
        }, SPAWN_TIMEOUT_MS);

        child.stdout.on('data', (data) => stdout += data.toString());
        child.stderr.on('data', (data) => stderr += data.toString());

        child.on('close', (code) => {
            clearTimeout(timer);
            if (killed) return;
            if (code === 0) {
                const cleanOut = stdout.replace(/\x1b\[[0-9;]*m/g, '').trim();
                resolve(cleanOut);
            } else {
                reject(new Error(`Agent Spawning Error (${agentId}): ${stderr}`));
            }
        });

        child.on('error', (err) => {
            clearTimeout(timer);
            reject(new Error(`Failed to spawn Python for agent ${agentId}: ${err.message}`));
        });
    });
}

// ─── Local System Tools ───────────────────────────────────────
const TOOLS = [
    {
        name: "readFile",
        description: "Read the full contents of a file at an absolute path. IMPORTANT: Use absolute paths.",
        input_schema: {
            type: "object",
            properties: {
                path: { type: "string", description: "Absolute path to the file to read" }
            },
            required: ["path"]
        }
    },
    {
        name: "writeFile",
        description: "Write content to a file. Overwrites the file if it exists. Creates parent directories if needed. IMPORTANT: Use absolute paths.",
        input_schema: {
            type: "object",
            properties: {
                path: { type: "string", description: "Absolute path to the file to write" },
                content: { type: "string", description: "The complete content to write to the file" }
            },
            required: ["path", "content"]
        }
    },
    {
        name: "runCommand",
        description: "Execute a shell command in the terminal. Use this to run scripts, curl endpoints, or verify syntax.",
        input_schema: {
            type: "object",
            properties: {
                command: { type: "string", description: "The shell command to run (e.g., 'node index.js', 'python script.py')" },
                cwd: { type: "string", description: "Optional current working directory for the command" }
            },
            required: ["command"]
        }
    },
    {
        name: "handOff",
        description: "Hand off control to a different agent species. Under the Iron Well Protocol, SFS-001 (Supervisor) must ALWAYS hand off execution to BE-001 (Backend) or FE-001 (Frontend) instead of writing code themselves.",
        input_schema: {
            type: "object",
            properties: {
                agentId: { type: "string", description: "The ID of the technical agent (e.g., 'BE-001', 'FE-001', 'QA-001')" },
                instructions: { type: "string", description: "Detailed execution plan and context for the new agent to follow" }
            },
            required: ["agentId", "instructions"]
        }
    },
    {
        name: "finishTask",
        description: "Call this tool exactly once when the entire task has been successfully verified and completed.",
        input_schema: {
            type: "object",
            properties: {
                summary: { type: "string", description: "Summary of what was achieved" }
            },
            required: ["summary"]
        }
    }
];

// ─── Tool Execution Handlers ──────────────────────────────────
async function executeTool(name, input, currentAgentId) {
    console.log(pc.gray(`\n  ⚙️  Tool Call: ${name}`));
    try {
        let result;
        if (name === 'readFile') {
            result = await fs.readFile(input.path, 'utf8');
        } else if (name === 'writeFile') {
            await fs.ensureDir(path.dirname(input.path));
            await fs.writeFile(input.path, input.content);
            result = `Successfully wrote to ${input.path}`;
        } else if (name === 'runCommand') {
            result = await new Promise((resolve) => {
                const child = spawn(input.command, {
                    shell: true,
                    cwd: input.cwd || process.cwd()
                });
                let out = '';
                child.stdout.on('data', d => out += d);
                child.stderr.on('data', d => out += d);
                child.on('close', code => {
                    resolve(`Exit Code: ${code}\nOutput:\n${out.trim().substring(0, 2000)}`);
                });
            });
        } else {
            result = `Unknown tool: ${name}`;
        }

        // Log the action
        await logAction(currentAgentId, name, input, result);
        return result;
    } catch (e) {
        return `Tool execution failed: ${e.message}`;
    }
}

// ─── Main Execution Loop ──────────────────────────────────────
async function runEngine(initialTask) {
    if (!process.env.ANTHROPIC_API_KEY) {
        console.log(pc.red('\n  ❌ Missing API Key in environment.'));
        console.log(pc.yellow('  Please set ANTHROPIC_API_KEY before running the engine.\n'));
        return;
    }

    console.log(pc.magenta(`\n🔥 Agent-Kit Autonomous Execution Engine v${PKG_VERSION}`));
    console.log(pc.gray(`   Model: ${AGENT_MODEL}`));

    // We strictly adhere to Iron Well Protocol: We always start with the Supervisor
    let currentAgentId = 'SFS-001';
    console.log(pc.cyan(`\n👤 Spawning Target Agent: ${currentAgentId} (Software Factory Supervisor)`));

    let systemPrompt = await getAgentPrompt(currentAgentId);

    // Maintain a message history for the LLM
    let messages = [
        { role: 'user', content: initialTask }
    ];

    let taskFinished = false;

    while (!taskFinished) {
        console.log(pc.yellow(`\n🧠 [${currentAgentId}] Thinking...`));

        try {
            const response = await anthropic.messages.create({
                model: AGENT_MODEL,
                max_tokens: 4096,
                system: systemPrompt,
                messages: messages,
                tools: TOOLS,
            });

            // Append assistant response to history
            messages.push({ role: 'assistant', content: response.content });

            for (const contentBlock of response.content) {
                if (contentBlock.type === 'text') {
                    console.log(pc.white(`\n🤖 [${currentAgentId}]:\n${contentBlock.text.trim()}`));
                } else if (contentBlock.type === 'tool_use') {
                    const toolName = contentBlock.name;
                    const toolInput = contentBlock.input;

                    if (toolName === 'finishTask') {
                        console.log(pc.green(`\n✅ Task Completed: ${toolInput.summary}\n`));
                        await logAction(currentAgentId, 'finishTask', toolInput, 'completed');
                        taskFinished = true;
                        break;
                    } else if (toolName === 'handOff') {
                        console.log(pc.blue(`\n🤝 Handoff Initiated: ${currentAgentId} -> ${toolInput.agentId}`));
                        console.log(pc.blue(`   Handover Notes: ${toolInput.instructions}`));

                        await logAction(currentAgentId, 'handOff', toolInput, `-> ${toolInput.agentId}`);

                        // Switch agent identity
                        currentAgentId = toolInput.agentId;
                        console.log(pc.cyan(`\n👤 Spawning Target Agent: ${currentAgentId}`));
                        systemPrompt = await getAgentPrompt(currentAgentId);

                        // Wipe history, but inject the supervisor's instructions as the new "user" task
                        messages = [
                            {
                                role: 'user',
                                content: `Your supervisor (SFS-001) has delegated execution to you. Here are your strict instructions:\n\n${toolInput.instructions}`
                            }
                        ];

                        break; // Break the content block loop, the while loop will repeat with the new agent
                    } else {
                        // Execute standard local tool
                        const result = await executeTool(toolName, toolInput, currentAgentId);

                        // Push tool result back to the model
                        messages.push({
                            role: 'user',
                            content: [
                                {
                                    type: 'tool_result',
                                    tool_use_id: contentBlock.id,
                                    content: result
                                }
                            ]
                        });
                    }
                }
            }
        } catch (error) {
            console.error(pc.red(`\n💥 Fatal Engine Error: ${error.message}`));
            await logAction(currentAgentId, 'FATAL_ERROR', { message: error.message }, 'crashed');
            break;
        }
    }
}

module.exports = runEngine;
