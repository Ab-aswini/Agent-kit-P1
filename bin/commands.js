const pc = require('picocolors');

// ─── Constants & Settings ─────────────────────────────────────
const COMMAND_PREFIX = '/';

// ─── Core Command Registry ────────────────────────────────────
// Maps commands to specific agents, descriptions, and prefix prompts.
const COMMAND_REGISTRY = {
    help: {
        description: 'List all available agent capabilities.',
        type: 'system',
        execute: (print) => {
            print(pc.cyan('\n🛠️  Available Slash Commands:'));
            Object.keys(COMMAND_REGISTRY).forEach(cmd => {
                const { description, agent } = COMMAND_REGISTRY[cmd];
                const badge = agent ? pc.gray(` [Agent: ${agent}]`) : '';
                print(`  ${pc.yellow(COMMAND_PREFIX + cmd)} - ${description}${badge}`);
            });
            print();
        }
    },
    fix: {
        description: 'Trigger the Error Analysis agent on the provided code/file.',
        type: 'agent',
        agent: 'QA-001', // Example: QA Engineer / Error Analyst
        systemPrompt: "You are a Senior Debugger. Analyze the following code or error for logical flaws and propose a precise fix:\n\n",
        color: pc.red
    },
    test: {
        description: 'Invoke the QA Agent to write unit tests.',
        type: 'agent',
        agent: 'QA-001', // Example: QA Engineer
        systemPrompt: "You are a Senior QA Automation Engineer. Write comprehensive, edge-case resilient unit tests for the following code:\n\n",
        color: pc.green
    },
    refactor: {
        description: 'Trigger the Architect agent to optimize and clean up code.',
        type: 'agent',
        agent: 'BE-001', // Example: Backend Architect
        systemPrompt: "You are a Senior Software Architect. Refactor the following code for maximum efficiency, readability, and adherence to SOLID principles:\n\n",
        color: pc.blue
    },
    plan: {
        description: 'Trigger the Strategy agent to build an implementation plan.',
        type: 'agent',
        agent: 'SP-001', // Example: Strategy Planner
        systemPrompt: "You are the Lead Strategy Planner. Decompose the following user request into a granular, step-by-step implementation plan:\n\n",
        color: pc.magenta
    },
    seo: {
        description: 'Trigger the SERAPH SEO+AEO agent for technical SEO, schema markup, and search optimization.',
        type: 'agent',
        agent: 'MKT-001', // SERAPH SEO+AEO Specialist
        systemPrompt: "You are the SERAPH SEO & AEO Specialist. Analyze the following request and provide actionable, deploy-ready SEO and AEO recommendations:\n\n",
        color: pc.cyan
    }
};

// ─── Dispatcher Layer ───────────────────────────────────────
class SlashDispatcher {
    constructor() {
        this.activeCommand = null;
    }

    /**
     * Parses user input to identify slash commands.
     * @param {string} input - Raw user input from terminal.
     * @returns {object} - { command, args, raw }
     */
    parse(input) {
        const trimmed = input.trim();
        if (!trimmed.startsWith(COMMAND_PREFIX)) {
            return { command: null, args: trimmed, raw: input, active: this.activeCommand };
        }

        const parts = trimmed.slice(1).split(' ');
        const potentialCmd = parts[0].toLowerCase();

        if (COMMAND_REGISTRY[potentialCmd]) {
            this.activeCommand = potentialCmd;
            const args = parts.slice(1).join(' ');
            return { command: potentialCmd, args, raw: input, active: this.activeCommand };
        }

        return { command: null, args: trimmed, raw: input, active: this.activeCommand };
    }

    /**
     * Resets the active command mode.
     */
    reset() {
        this.activeCommand = null;
    }

    /**
     * Builds the final dispatched prompt.
     */
    dispatch(parsedInput, spawnAgentFn) {
        const { command, args, active } = parsedInput;

        // If it's a direct system command (like /help)
        if (command && COMMAND_REGISTRY[command].type === 'system') {
            COMMAND_REGISTRY[command].execute(console.log);
            this.reset();
            return null; // Signals the REPL to not process further
        }

        // If we are evaluating an agent command
        const currentTrigger = command || active;

        if (currentTrigger && COMMAND_REGISTRY[currentTrigger]) {
            const cmdDef = COMMAND_REGISTRY[currentTrigger];

            // Build the injected/wrapped prompt
            const injectedPrompt = `${cmdDef.systemPrompt}${args}`;

            // In a fully integrated system with LLM execution, 
            // you would pass `injectedPrompt` & `cmdDef.agent` to the LLM router here.
            // For now, since Agent-Kit is headless, we generate the full prompt using spawn_agent.py logic.

            return {
                agentId: cmdDef.agent,
                injectedPrompt,
                badgeColor: cmdDef.color,
                commandName: currentTrigger
            };
        }

        // Standard chat routing (no command active)
        return {
            agentId: 'SFS-001', // Default to Senior Full Stack 
            injectedPrompt: args,
            badgeColor: pc.white,
            commandName: 'chat'
        };
    }

    /**
     * Get the styled badge for the active command.
     */
    getBadge() {
        if (!this.activeCommand) return pc.gray('💬');
        const cmdDef = COMMAND_REGISTRY[this.activeCommand];
        const colorFn = cmdDef.color || pc.cyan;
        return pc.inverse(colorFn(` ${this.activeCommand.toUpperCase()} `));
    }
}

module.exports = { SlashDispatcher, COMMAND_REGISTRY };
