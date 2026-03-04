#!/usr/bin/env node
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { CallToolRequestSchema, ListToolsRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const { spawn } = require('child_process');
const path = require('path');

// Read version from package.json so it always stays in sync
const PKG_VERSION = require('../package.json').version;

const server = new Server(
    {
        name: "agent-kit",
        version: PKG_VERSION,
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// ─── Unified Script Runner ──────────────────────────────────────────────────
// Replaces the 3 near-identical helpers (runSpawnScript, runUIDesignScript, runPythonScript)
const SCRIPT_TIMEOUT_MS = 30_000; // 30 seconds

/**
 * Runs a Python script and returns its stdout/stderr.
 * @param {string} scriptPath - Absolute path to the Python script.
 * @param {string[]} args - Arguments to pass to the script.
 * @param {object} opts
 * @param {string} [opts.cwd] - Working directory (defaults to sourceDir).
 * @param {boolean} [opts.mergeStderr] - If true, merge stderr into output (for scripts like checklist.py that report errors as text).
 * @returns {Promise<string>} Cleaned stdout output.
 */
function runScript(scriptPath, args = [], opts = {}) {
    return new Promise((resolve, reject) => {
        const cwd = opts.cwd || path.join(__dirname, '..');
        const child = spawn('python', [scriptPath, ...args], { cwd });

        let stdout = '';
        let stderr = '';
        let killed = false;

        // Timeout guard — prevents hung scripts from blocking the MCP server forever
        const timer = setTimeout(() => {
            killed = true;
            child.kill('SIGTERM');
            reject(new Error(`Script timed out after ${SCRIPT_TIMEOUT_MS / 1000}s: ${path.basename(scriptPath)}`));
        }, SCRIPT_TIMEOUT_MS);

        child.stdout.on('data', (data) => stdout += data.toString());
        child.stderr.on('data', (data) => stderr += data.toString());

        child.on('close', (code) => {
            clearTimeout(timer);
            if (killed) return; // already rejected by timeout

            // Strip ANSI color codes for clean IDE output
            const strip = (s) => s.replace(/\x1b\[[0-9;]*m/g, '').trim();

            if (opts.mergeStderr) {
                // Scripts like checklist.py/security_chaos_test.py may exit non-zero
                // but their output is still valuable for the LLM
                resolve(strip(stdout + '\n' + stderr));
            } else if (code === 0) {
                resolve(strip(stdout));
            } else {
                reject(new Error(`Script error (exit ${code}): ${strip(stderr)}`));
            }
        });

        child.on('error', (err) => {
            clearTimeout(timer);
            reject(err);
        });
    });
}

// ─── Resolved script paths ──────────────────────────────────────────────────
const SOURCE_DIR = path.join(__dirname, '..');
const SCRIPTS = {
    spawn: path.join(SOURCE_DIR, 'scripts', 'spawn_agent.py'),
    uiux: path.join(SOURCE_DIR, '.agent-os', '.shared', 'UI&UX', 'scripts', 'design_system.py'),
    audit: path.join(SOURCE_DIR, 'scripts', 'checklist.py'),
    security: path.join(SOURCE_DIR, 'scripts', 'security_chaos_test.py'),
    memory: path.join(SOURCE_DIR, 'scripts', 'memory_sync.py'),
};

// ─── Tool Definitions ────────────────────────────────────────────────────────
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "list_agents",
                description: "List all available AI agents in the Agent-Kit system, returning their IDs and descriptions.",
                inputSchema: {
                    type: "object",
                    properties: {
                        department: {
                            type: "string",
                            description: "Optional department filter (e.g., 'backend', 'frontend', 'qa')"
                        }
                    }
                }
            },
            {
                name: "get_agent_prompt",
                description: "Generate the full system prompt for a specific agent (e.g., 'CTS-001', 'BE-001'). Use this to adopt the agent's persona.",
                inputSchema: {
                    type: "object",
                    properties: {
                        agentId: {
                            type: "string",
                            description: "The ID of the agent to spawn (e.g., 'SFS-001', 'BE-003', 'QA-001')"
                        }
                    },
                    required: ["agentId"]
                }
            },
            {
                name: "query_ui_ux_engine",
                description: "Generates a complete design system and architectural recommendations based on real-world SaaS templates using FTS5 search. Returns Markdown output with tokens, palettes, and rules.",
                inputSchema: {
                    type: "object",
                    properties: {
                        query: {
                            type: "string",
                            description: "The search query, e.g., 'SaaS dashboard', 'fintech mobile app'."
                        },
                        projectName: {
                            type: "string",
                            description: "Optional name of the project."
                        }
                    },
                    required: ["query"]
                }
            },
            {
                name: "run_project_audit",
                description: "Runs the complete Agent-Kit system health check and architecture audit (checklist.py). Use this to verify project integrity, missing components, or zero-footprint compliance.",
                inputSchema: {
                    type: "object",
                    properties: {} // No arguments required
                }
            },
            {
                name: "run_security_chaos",
                description: "Runs the Security Chaos Monkey (security_chaos_test.py) to scan for exposed credentials, risky eval() statements, and dangerous shell executions.",
                inputSchema: {
                    type: "object",
                    properties: {} // No arguments required
                }
            },
            {
                name: "sync_semantic_memory",
                description: "Triggers a real-time AST parse of the user's project to extract the active architecture, API routes, and dependencies into memory/global/. Use this to ensure you have the absolute ground-truth context before writing complex plans or starting work.",
                inputSchema: {
                    type: "object",
                    properties: {}
                }
            }
        ],
    };
});

// ─── Tool Execution ──────────────────────────────────────────────────────────
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const userCwd = process.cwd();

    try {
        switch (name) {
            case "list_agents": {
                const department = args?.department;
                const scriptArgs = department ? ['--list', '--dept', department] : ['--list'];
                const output = await runScript(SCRIPTS.spawn, scriptArgs);
                return { content: [{ type: "text", text: output }] };
            }
            case "get_agent_prompt": {
                const agentId = args?.agentId;
                if (!agentId) throw new Error("agentId is required");
                const output = await runScript(SCRIPTS.spawn, [agentId]);
                return { content: [{ type: "text", text: output }] };
            }
            case "query_ui_ux_engine": {
                const query = args?.query;
                if (!query) throw new Error("query is required");
                const scriptArgs = [query, '--format', 'markdown'];
                if (args?.projectName) scriptArgs.push('--project-name', args.projectName);
                const output = await runScript(SCRIPTS.uiux, scriptArgs);
                return { content: [{ type: "text", text: output }] };
            }
            case "run_project_audit": {
                const output = await runScript(SCRIPTS.audit, [], { cwd: userCwd, mergeStderr: true });
                return { content: [{ type: "text", text: output }] };
            }
            case "run_security_chaos": {
                const output = await runScript(SCRIPTS.security, [], { cwd: userCwd, mergeStderr: true });
                return { content: [{ type: "text", text: output }] };
            }
            case "sync_semantic_memory": {
                const output = await runScript(SCRIPTS.memory, [], { cwd: userCwd, mergeStderr: true });
                return { content: [{ type: "text", text: output }] };
            }
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    } catch (error) {
        return {
            content: [{ type: "text", text: `Error in ${name}: ${error.message}` }],
            isError: true,
        };
    }
});

// ─── Server Startup ──────────────────────────────────────────────────────────
async function startMcpServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error(`Agent-Kit MCP Server v${PKG_VERSION} running on stdio`);
}

startMcpServer().catch((error) => {
    console.error("Fatal error in MCP Server:", error);
    process.exit(1);
});
