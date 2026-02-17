#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');

const args = process.argv.slice(2);
const command = args[0];

const sourceDir = path.join(__dirname, '..');
const targetDir = process.cwd();

async function doctor() {
    console.log(pc.cyan('\n🩺 Running Agent-Kit Health Check...'));
    const required = ['.agent-os', 'docs', 'memory', 'scripts', 'manifest.json'];
    let issues = 0;

    for (const folder of required) {
        const p = path.join(targetDir, folder);
        if (!await fs.pathExists(p)) {
            console.log(pc.red(`  ❌ Missing: ${folder}`));
            issues++;
        } else {
            console.log(pc.green(`  ✅ Found: ${folder}`));
        }
    }

    if (issues === 0) {
        console.log(pc.green('\n✨ System is Healthy! All core structures verified.'));
    } else {
        console.log(pc.yellow(`\n⚠️ Found ${issues} potential issues. Consider running 'init' again.`));
    }
}

async function smartMergePackageJson(sourceDir, targetDir) {
    const srcPkg = path.join(sourceDir, 'package.json');
    const destPkg = path.join(targetDir, 'package.json');

    if (!await fs.pathExists(destPkg)) {
        await fs.copy(srcPkg, destPkg);
        return;
    }

    console.log(pc.gray('  Merging package.json dependencies...'));
    const src = await fs.readJson(srcPkg);
    const dest = await fs.readJson(destPkg);

    // Merge dependencies
    dest.dependencies = { ...dest.dependencies, ...src.dependencies };
    dest.devDependencies = { ...dest.devDependencies, ...src.devDependencies };

    // Add scripts if missing, but prefer target scripts if overlap
    dest.scripts = { ...src.scripts, ...dest.scripts };

    await fs.writeJson(destPkg, dest, { spaces: 4 });
}

async function init() {
    console.log(pc.cyan('\n🚀 Initializing Agent-Kit...'));

    const foldersToCopy = ['.agent-os', 'docs', 'memory', 'src', 'scripts'];

    try {
        // 1. Smart Merge package.json
        await smartMergePackageJson(sourceDir, targetDir);

        // 2. Sync core folders
        for (const folder of foldersToCopy) {
            const src = path.join(sourceDir, folder);
            const dest = path.join(targetDir, folder);

            if (await fs.pathExists(src)) {
                console.log(pc.gray(`  Syncing ${folder}...`));
                await fs.copy(src, dest, { overwrite: true, errorOnExist: false });
            }
        }

        // 3. Copy top-level metadata
        const filesToCopy = ['manifest.json', 'METADATA.md', 'PROJECT_STATUS.md'];
        for (const file of filesToCopy) {
            const src = path.join(sourceDir, file);
            const dest = path.join(targetDir, file);
            if (await fs.pathExists(src)) {
                await fs.copy(src, dest);
            }
        }

        console.log(pc.green('\n✅ Agent-Kit initialized successfully!'));
        console.log(pc.white('\nNext steps:'));
        console.log(pc.gray('  1. Open the project in your AI-powered IDE.'));
        console.log(pc.gray('  2. Run "npx @ab-aswini/agent-kit-p1 doctor" to verify.'));
        console.log(pc.gray('  3. Instruct your AI to read .agent-os/agents/tier-1/chief-technical-supervisor.agent.md.'));
    } catch (err) {
        console.error(pc.red('\n❌ Error during initialization:'), err.message);
        process.exit(1);
    }
}

// Command Router
if (command === 'doctor') {
    doctor();
} else if (command === 'init' || !command) {
    init();
} else {
    console.log(pc.yellow(`Unknown command: ${command}`));
    console.log('Available commands: init, doctor');
    console.log('Usage: npx @ab-aswini/agent-kit-p1 init');
}
