const { spawn } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');
const os = require('os');

// ─── Configuration ────────────────────────────────────────────
const PKG_VERSION = require('../package.json').version;
const SPAWN_TIMEOUT_MS = 30_000;

// ─── Action Logger ────────────────────────────────────────────
// Logs are stored in the Agent-Kit source (not user project) for audit traceability.
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

// ─── Supportive Office Engine ─────────────────────────────────
// Agent-Kit does NOT make external LLM API calls.
// This engine generates a rich, structured system prompt for your IDE's native AI
// (Google Antigravity, Copilot, Claude, etc.) to execute the task intelligently.
async function runEngine(initialTask) {
    console.log(pc.magenta(`\n🏢 Agent-Kit Supportive Office Engine v${PKG_VERSION}`));
    console.log(pc.gray(`   Generating structured agent context for your IDE's AI...\n`));

    // We always start with the SFS-001 Supervisor under the Iron Well Protocol
    const currentAgentId = 'SFS-001';
    console.log(pc.cyan(`\n👤 Loading Agent: ${currentAgentId} (Senior Full-Stack Supervisor)`));

    let systemPrompt;
    try {
        systemPrompt = await getAgentPrompt(currentAgentId);
    } catch (err) {
        console.error(pc.red(`\n❌ Error generating agent prompt: ${err.message}`));
        return;
    }

    await logAction(currentAgentId, 'runEngine', { task: initialTask }, 'prompt_generated');

    // Output the structured context block for the user to paste into their IDE AI
    const separator = '─'.repeat(60);

    console.log(pc.yellow(`\n${separator}`));
    console.log(pc.bold(pc.white('📋 AGENT SYSTEM PROMPT (paste into your IDE AI):')));
    console.log(pc.yellow(separator));
    console.log(pc.white('\n[SYSTEM ROLE — SFS-001]\n'));
    console.log(pc.gray(systemPrompt.substring(0, 1500) + (systemPrompt.length > 1500 ? '\n... [truncated — full prompt available via: agent-kit mcp → get_agent_prompt]' : '')));
    console.log(pc.yellow(`\n${separator}`));
    console.log(pc.bold(pc.white('📝 USER TASK:')));
    console.log(pc.yellow(separator));
    console.log(pc.white(`\n${initialTask}\n`));
    console.log(pc.yellow(separator));

    console.log(pc.green(`\n✅ Context package ready!`));
    console.log(pc.white(`\n💡 Next Steps:`));
    console.log(pc.gray(`  1. Copy the SYSTEM PROMPT above into your IDE AI's system context.`));
    console.log(pc.gray(`  2. The AI will now operate as SFS-001 and invoke Iron Well Protocol.`));
    console.log(pc.gray(`  3. For native integration, use the MCP server: agent-kit mcp\n`));
}

module.exports = runEngine;
