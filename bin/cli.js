#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const pc = require('picocolors');
const readline = require('readline');

const args = process.argv.slice(2);
const command = args[0];
const isInteractive = args.includes('--interactive') || args.includes('-i');

const sourceDir = path.join(__dirname, '..');
const targetDir = process.cwd();

// ─── Interactive Prompt Helper ───────────────────────────────
function ask(rl, question) {
    return new Promise(resolve => rl.question(question, resolve));
}

// ─── Doctor Command ──────────────────────────────────────────
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

// ─── Smart Merge Package.json ────────────────────────────────
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

    dest.dependencies = { ...dest.dependencies, ...src.dependencies };
    dest.devDependencies = { ...dest.devDependencies, ...src.devDependencies };
    dest.scripts = { ...src.scripts, ...dest.scripts };

    await fs.writeJson(destPkg, dest, { spaces: 4 });
}

// ─── Interactive Archetype Selection ─────────────────────────
async function selectArchetype() {
    const archetypesDir = path.join(sourceDir, '.agent-os', 'templates', 'archetypes');
    const archetypeFiles = await fs.readdir(archetypesDir);
    const archetypes = [];

    for (const file of archetypeFiles) {
        if (file.endsWith('.json')) {
            const data = await fs.readJson(path.join(archetypesDir, file));
            archetypes.push({ file, ...data });
        }
    }

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    console.log(pc.cyan('\n🏗️  Agent-Kit Interactive Setup\n'));
    console.log(pc.white('Choose your company archetype:\n'));
    archetypes.forEach((a, i) => {
        console.log(pc.yellow(`  [${i + 1}] ${a.name}`));
        console.log(pc.gray(`      ${a.description}\n`));
    });
    console.log(pc.yellow(`  [${archetypes.length + 1}] Full Fleet (all 53 agents)\n`));

    const answer = await ask(rl, pc.white('Enter your choice (number): '));
    rl.close();

    const choice = parseInt(answer, 10);
    if (choice >= 1 && choice <= archetypes.length) {
        return archetypes[choice - 1];
    }
    return null; // Full fleet
}

// ─── Selective Agent Copy ────────────────────────────────────
async function copySelectedAgents(archetype) {
    const agentsSource = path.join(sourceDir, '.agent-os', 'agents');
    const agentsDest = path.join(targetDir, '.agent-os', 'agents');

    // Always copy tier-1 (executive)
    const tier1Src = path.join(agentsSource, 'tier-1');
    const tier1Dest = path.join(agentsDest, 'tier-1');
    if (await fs.pathExists(tier1Src)) {
        await fs.copy(tier1Src, tier1Dest, { overwrite: true });
    }

    // Map department keys to folder paths
    const deptFolderMap = {
        'engineering_backend': 'engineering/backend',
        'engineering_frontend': 'engineering/frontend',
        'engineering_database': 'engineering/database',
        'engineering_game': 'engineering/game',
        'engineering_mobile': 'engineering/mobile',
        'devops': 'devops',
        'security': 'security',
        'qa': 'qa',
        'product': 'product',
        'marketing': 'marketing-growth',
        'meta': 'meta',
        'intelligence': 'intelligence'
    };

    for (const dept of archetype.departments) {
        const folder = deptFolderMap[dept];
        if (!folder) continue;

        const src = path.join(agentsSource, folder);
        const dest = path.join(agentsDest, folder);
        if (await fs.pathExists(src)) {
            console.log(pc.gray(`  Syncing agents: ${dept}...`));
            await fs.copy(src, dest, { overwrite: true });
        }
    }
}

// ─── Selective Skills Copy ───────────────────────────────────
async function copySelectedSkills(archetype) {
    const skillsSource = path.join(sourceDir, '.agent-os', 'skills');
    const skillsDest = path.join(targetDir, '.agent-os', 'skills');

    if (!archetype.requiredSkills) {
        // Copy all skills
        await fs.copy(skillsSource, skillsDest, { overwrite: true });
        return;
    }

    // Always copy essential standalone files
    const essentialFiles = ['doc.md', 'democracy-protocol.skill.md', 'memory-compression.skill.md'];
    for (const file of essentialFiles) {
        const src = path.join(skillsSource, file);
        const dest = path.join(skillsDest, file);
        if (await fs.pathExists(src)) {
            await fs.copy(src, dest, { overwrite: true });
        }
    }

    // Always copy clean-code and brainstorming (universal)
    const universalSkills = ['clean-code', 'brainstorming', 'intelligent-routing', 'behavioral-modes'];
    const allSkills = [...universalSkills, ...archetype.requiredSkills];

    for (const skill of allSkills) {
        const src = path.join(skillsSource, skill);
        const dest = path.join(skillsDest, skill);
        if (await fs.pathExists(src)) {
            console.log(pc.gray(`  Syncing skill: ${skill}...`));
            await fs.copy(src, dest, { overwrite: true });
        }
    }
}

// ─── Init Command ────────────────────────────────────────────
async function init() {
    let archetype = null;

    if (isInteractive) {
        archetype = await selectArchetype();
        if (archetype) {
            console.log(pc.green(`\n✅ Selected: ${archetype.name}`));
            console.log(pc.gray(`   ${archetype.agents.length} agents | ${archetype.departments.length} departments\n`));
        } else {
            console.log(pc.green('\n✅ Selected: Full Fleet (53 agents)\n'));
        }
    }

    console.log(pc.cyan('🚀 Initializing Agent-Kit...'));

    try {
        // 1. Smart Merge package.json
        await smartMergePackageJson(sourceDir, targetDir);

        if (archetype) {
            // ── SELECTIVE MODE ──
            // Copy rules, configs, templates, and selected structure
            const coreFolders = ['rules', 'configs', 'templates', 'workflows', 'logs', 'scripts', '.shared'];
            for (const folder of coreFolders) {
                const src = path.join(sourceDir, '.agent-os', folder);
                const dest = path.join(targetDir, '.agent-os', folder);
                if (await fs.pathExists(src)) {
                    await fs.copy(src, dest, { overwrite: true });
                }
            }

            // Copy hub-logic.md
            const hubSrc = path.join(sourceDir, '.agent-os', 'hub-logic.md');
            const hubDest = path.join(targetDir, '.agent-os', 'hub-logic.md');
            if (await fs.pathExists(hubSrc)) {
                await fs.copy(hubSrc, hubDest, { overwrite: true });
            }

            // Selective agents
            await copySelectedAgents(archetype);

            // Selective skills
            await copySelectedSkills(archetype);

            // Copy other top-level folders
            const topFolders = ['docs', 'memory', 'src', 'scripts'];
            for (const folder of topFolders) {
                const src = path.join(sourceDir, folder);
                const dest = path.join(targetDir, folder);
                if (await fs.pathExists(src)) {
                    console.log(pc.gray(`  Syncing ${folder}...`));
                    await fs.copy(src, dest, { overwrite: true });
                }
            }
        } else {
            // ── FULL MODE (default / backwards compatible) ──
            const foldersToCopy = ['.agent-os', 'docs', 'memory', 'src', 'scripts'];
            for (const folder of foldersToCopy) {
                const src = path.join(sourceDir, folder);
                const dest = path.join(targetDir, folder);
                if (await fs.pathExists(src)) {
                    console.log(pc.gray(`  Syncing ${folder}...`));
                    await fs.copy(src, dest, { overwrite: true, errorOnExist: false });
                }
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

        const agentCount = archetype ? archetype.agents.length : 53;
        console.log(pc.green(`\n✅ Agent-Kit initialized successfully! (${agentCount} agents deployed)`));
        console.log(pc.white('\nNext steps:'));
        console.log(pc.gray('  1. Open the project in your AI-powered IDE.'));
        console.log(pc.gray('  2. Run "npx @ab-aswini/agent-kit-p1 doctor" to verify.'));
        console.log(pc.gray('  3. Instruct your AI to read .agent-os/agents/tier-1/chief-technical-supervisor.agent.md.'));

        if (archetype) {
            console.log(pc.gray(`\n  💡 Archetype: ${archetype.name}`));
            console.log(pc.gray(`  📦 To switch to full fleet later: npx @ab-aswini/agent-kit-p1 init`));
        }
    } catch (err) {
        console.error(pc.red('\n❌ Error during initialization:'), err.message);
        process.exit(1);
    }
}

// ─── Command Router ──────────────────────────────────────────
if (command === 'doctor') {
    doctor();
} else if (command === 'init' || !command) {
    init();
} else {
    console.log(pc.yellow(`Unknown command: ${command}`));
    console.log('Available commands: init, doctor');
    console.log('Usage: npx @ab-aswini/agent-kit-p1 init');
    console.log('       npx @ab-aswini/agent-kit-p1 init --interactive');
}
