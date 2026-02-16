#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');

const args = process.argv.slice(2);
const command = args[0];

const sourceDir = path.join(__dirname, '..');
const targetDir = process.cwd();

async function init() {
    console.log(pc.cyan('\n🚀 Initializing Agent-Kit...'));

    const foldersToCopy = ['.agent-os', 'docs', 'memory', 'src', 'scripts'];

    try {
        for (const folder of foldersToCopy) {
            const src = path.join(sourceDir, folder);
            const dest = path.join(targetDir, folder);

            if (await fs.pathExists(src)) {
                console.log(pc.gray(`  Copying ${folder}...`));
                await fs.copy(src, dest, { overwrite: false, errorOnExist: false });
            }
        }

        console.log(pc.green('\n✅ Agent-Kit initialized successfully!'));
        console.log(pc.white('\nNext steps:'));
        console.log(pc.gray('  1. Open the project in your AI-powered IDE.'));
        console.log(pc.gray('  2. Instruct your AI to read .agent-os/agents/tier-1/chief-technical-supervisor.agent.md.'));
        console.log(pc.gray('  3. Start building with your 53-agent fleet.\n'));
    } catch (err) {
        console.error(pc.red('\n❌ Error initializing Agent-Kit:'), err.message);
        process.exit(1);
    }
}

if (command === 'init' || !command) {
    init();
} else {
    console.log(pc.yellow(`Unknown command: ${command}`));
    console.log('Use "npx @ab-aswini/agent-kit-p1 init" to set up the project.');
}
