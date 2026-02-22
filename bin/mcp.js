#!/usr/bin/env node
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { CallToolRequestSchema, ListToolsRequestSchema } = require("@modelcontextprotocol/sdk/types.js");
const { spawn } = require('child_process');
const path = require('path');

const server = new Server(
    {
        name: "agent-kit",
        version: "3.0.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

// Define tools available
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "list_agents",
                description: "List all available 53 AI agents in the Agent-Kit system, returning their abbreviations and descriptions.",
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
                description: "Generates a complete design system and architectural recommendations based on real-world SaaS templates using a custom BM25 vector search. Returns Markdown output with tokens, palettes, and rules.",
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
            }
        ],
    };
});

// Helper function to run the python orchestrator
async function runSpawnScript(args) {
    return new Promise((resolve, reject) => {
        // Resolve script relative to this file
        const sourceDir = path.join(__dirname, '..');
        const scriptPath = path.join(sourceDir, 'scripts', 'spawn_agent.py');

        const process = spawn('python', [scriptPath, ...args]);

        let stdout = '';
        let stderr = '';

        process.stdout.on('data', (data) => stdout += data.toString());
        process.stderr.on('data', (data) => stderr += data.toString());

        process.on('close', (code) => {
            if (code === 0) {
                // Remove some of the terminal color codes if present so the IDE reads it cleanly
                const cleanOut = stdout.replace(/\x1b\[[0-9;]*m/g, '').trim();
                resolve(cleanOut);
            } else {
                reject(new Error(`Agent-Kit Script Error: ${stderr}`));
            }
        });

        process.on('error', (err) => {
            reject(err);
        });
    });
}

// Helper for UI/UX Python engine
async function runUIDesignScript(args) {
    return new Promise((resolve, reject) => {
        const sourceDir = path.join(__dirname, '..');
        const scriptPath = path.join(sourceDir, '.agent-os', '.shared', 'UI&UX', 'scripts', 'design_system.py');

        const process = spawn('python', [scriptPath, ...args]);

        let stdout = '';
        let stderr = '';

        process.stdout.on('data', (data) => stdout += data.toString());
        process.stderr.on('data', (data) => stderr += data.toString());

        process.on('close', (code) => {
            if (code === 0) {
                // Strip ansi colors
                const cleanOut = stdout.replace(/\x1b\[[0-9;]*m/g, '').trim();
                resolve(cleanOut);
            } else {
                reject(new Error(`UI/UX Engine Error: ${stderr}`));
            }
        });

        process.on('error', (err) => {
            reject(err);
        });
    });
}

// Helper to run any arbitrary python script in the scripts/ directory
async function runPythonScript(scriptName) {
    return new Promise((resolve, reject) => {
        const sourceDir = path.join(__dirname, '..');
        const scriptPath = path.join(sourceDir, 'scripts', scriptName);

        // Ensure Python runs in the EXACT directory the user launched from (where their project is)
        const userProjectDir = process.cwd();
        const processRef = spawn('python', [scriptPath], { cwd: userProjectDir });

        let stdout = '';
        let stderr = '';

        processRef.stdout.on('data', (data) => stdout += data.toString());
        processRef.stderr.on('data', (data) => stderr += data.toString());

        processRef.on('close', (code) => {
            // Some scripts might exit with code 1 if they find errors (e.g. security flaws). 
            // We want to return the output regardless so the LLM can see the errors.
            const cleanOut = (stdout + '\n' + stderr).replace(/\x1b\[[0-9;]*m/g, '').trim();
            resolve(cleanOut);
        });

        process.on('error', (err) => {
            reject(err);
        });
    });
}

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    switch (request.params.name) {
        case "list_agents": {
            const department = request.params.arguments?.department;
            const args = department ? ['--list', '--dept', department] : ['--list'];
            try {
                const output = await runSpawnScript(args);
                return {
                    content: [{ type: "text", text: output }]
                };
            } catch (error) {
                return {
                    content: [{ type: "text", text: `Error listing agents: ${error.message}` }],
                    isError: true,
                };
            }
        }
        case "get_agent_prompt": {
            const agentId = request.params.arguments?.agentId;
            if (!agentId) {
                throw new Error("agentId is required");
            }
            try {
                // Pass the agentId directly to spawn_agent.py
                const output = await runSpawnScript([agentId]);
                return {
                    content: [{ type: "text", text: output }]
                };
            } catch (error) {
                return {
                    content: [{ type: "text", text: `Error generating prompt for ${agentId}: ${error.message}` }],
                    isError: true,
                };
            }
        }
        case "query_ui_ux_engine": {
            const queryParam = request.params.arguments?.query;
            const projectName = request.params.arguments?.projectName;
            if (!queryParam) {
                throw new Error("query is required");
            }
            try {
                const args = [queryParam, '--format', 'markdown'];
                if (projectName) {
                    args.push('--project-name', projectName);
                }
                const output = await runUIDesignScript(args);
                return {
                    content: [{ type: "text", text: output }]
                };
            } catch (error) {
                return {
                    content: [{ type: "text", text: `Error querying UI/UX Engine: ${error.message}` }],
                    isError: true,
                };
            }
        }
        case "run_project_audit": {
            try {
                const output = await runPythonScript('checklist.py');
                return {
                    content: [{ type: "text", text: output }]
                };
            } catch (error) {
                return {
                    content: [{ type: "text", text: `Error running project audit: ${error.message}` }],
                    isError: true,
                };
            }
        }
        case "run_security_chaos": {
            try {
                const output = await runPythonScript('security_chaos_test.py');
                return {
                    content: [{ type: "text", text: output }]
                };
            } catch (error) {
                return {
                    content: [{ type: "text", text: `Error running security chaos: ${error.message}` }],
                    isError: true,
                };
            }
        }
        default:
            throw new Error(`Unknown tool: ${request.params.name}`);
    }
});

// Start the server
async function startMcpServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Agent-Kit MCP Server running on stdio");
}

startMcpServer().catch((error) => {
    console.error("Fatal error in MCP Server:", error);
    process.exit(1);
});
