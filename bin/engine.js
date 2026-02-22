const { Anthropic } = require('@anthropic-ai/sdk');
const { spawn } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');

// Load environment variables if they exist (e.g., ANTHROPIC_API_KEY)
require('dotenv').config();

const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY || ''
});

// Generate System Prompt from our Zero-Footprint Global Store
async function getAgentPrompt(agentId) {
    return new Promise((resolve, reject) => {
        const sourceDir = path.join(__dirname, '..');
        const scriptPath = path.join(sourceDir, 'scripts', 'spawn_agent.py');

        const process = spawn('python', [scriptPath, agentId]);

        let stdout = '';
        let stderr = '';

        process.stdout.on('data', (data) => stdout += data.toString());
        process.stderr.on('data', (data) => stderr += data.toString());

        process.on('close', (code) => {
            if (code === 0) {
                const cleanOut = stdout.replace(/\x1b\[[0-9;]*m/g, '').trim();
                resolve(cleanOut);
            } else {
                reject(new Error(`Agent Spawning Error: ${stderr}`));
            }
        });
    });
}

// Local System Tools
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

// Tool Execution Handlers
async function executeTool(name, input) {
    console.log(pc.gray(`\n  ⚙️  Tool Call: ${name}`));
    try {
        if (name === 'readFile') {
            const content = await fs.readFile(input.path, 'utf8');
            return content;
        } else if (name === 'writeFile') {
            await fs.ensureDir(path.dirname(input.path));
            await fs.writeFile(input.path, input.content);
            return `Successfully wrote to ${input.path}`;
        } else if (name === 'runCommand') {
            return new Promise((resolve) => {
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
        }
        return `Unknown tool: ${name}`;
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

    console.log(pc.magenta('\n🔥 Agent-Kit Autonomous Execution Engine Activating...'));

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
                model: 'claude-3-5-sonnet-latest',
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
                        taskFinished = true;
                        break;
                    } else if (toolName === 'handOff') {
                        console.log(pc.blue(`\n🤝 Handoff Initiated: ${currentAgentId} -> ${toolInput.agentId}`));
                        console.log(pc.blue(`   Handover Notes: ${toolInput.instructions}`));

                        // Switch agent identity
                        currentAgentId = toolInput.agentId;
                        console.log(pc.cyan(`\n👤 Spawning Target Agent: ${currentAgentId}`));
                        systemPrompt = await getAgentPrompt(currentAgentId);

                        // Wipe history, but inject the supervisor's instructions as the new "user" task 
                        // so the sub-agent knows exactly what to do.
                        messages = [
                            {
                                role: 'user',
                                content: `Your supervisor (SFS-001) has delegated execution to you. Here are your strict instructions:\n\n${toolInput.instructions}`
                            }
                        ];

                        // Acknowledge the tool use from the PREVIOUS agent's perspective before wiping
                        // Note: Because we wiped the context for the new agent, the previous agent's loop technically ends here for now
                        break; // Break the content block loop, the while loop will repeat with the new agent
                    } else {
                        // Execute standard local tool
                        const result = await executeTool(toolName, toolInput);

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
            break;
        }
    }
}

module.exports = runEngine;
