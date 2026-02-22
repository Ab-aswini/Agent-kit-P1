#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const crypto = require('crypto');
const os = require('os');
const pc = require('picocolors');
const readline = require('readline');
const { spawn } = require('child_process');
const { SlashDispatcher } = require('./commands');

const args = process.argv.slice(2);
const command = args[0];
const isInteractive = args.includes('--interactive') || args.includes('-i');

const sourceDir = path.join(__dirname, '..');
const targetDir = process.cwd();

// ─── Global Store Paths ─────────────────────────────────────
const GLOBAL_STORE_ROOT = path.join(os.homedir(), '.agent-os', 'projects');
const POINTER_FILENAME = '.agentkit';

function getProjectHash(projectPath) {
    return crypto.createHash('sha256').update(projectPath).digest('hex').slice(0, 12);
}

function getGlobalStorePath(projectPath) {
    const hash = getProjectHash(projectPath);
    return path.join(GLOBAL_STORE_ROOT, hash);
}

function getPointerFilePath(projectPath) {
    return path.join(projectPath, POINTER_FILENAME);
}

// ─── .agentkit Pointer I/O ──────────────────────────────────
function buildPointerConfig(projectPath, storePath) {
    const normalize = (p) => p.replace(/\\/g, '/');
    return {
        version: '2.0.0',
        store: normalize(storePath),
        paths: {
            agents: normalize(path.join(storePath, '.agent-os', 'agents')),
            rules: normalize(path.join(storePath, '.agent-os', 'rules')),
            skills: normalize(path.join(storePath, '.agent-os', 'skills')),
            configs: normalize(path.join(storePath, '.agent-os', 'configs')),
            config: normalize(path.join(storePath, '.agent-os', 'config')),
            templates: normalize(path.join(storePath, '.agent-os', 'templates')),
            workflows: normalize(path.join(storePath, '.agent-os', 'workflows')),
            shared: normalize(path.join(storePath, '.agent-os', '.shared')),
            logs: normalize(path.join(storePath, '.agent-os', 'logs')),
            memory: normalize(path.join(storePath, 'memory')),
            docs: normalize(path.join(storePath, 'docs')),
            scripts: normalize(path.join(storePath, 'scripts')),
        },
        project: normalize(projectPath),
        created: new Date().toISOString(),
    };
}

async function readPointer(projectPath) {
    const pointerPath = getPointerFilePath(projectPath);
    if (await fs.pathExists(pointerPath)) {
        try {
            return await fs.readJson(pointerPath);
        } catch {
            return null;
        }
    }
    return null;
}

// ─── Interactive Prompt Helper ───────────────────────────────
function ask(rl, question) {
    return new Promise(resolve => rl.question(question, resolve));
}

// ─── Interactive Archetype Selection ─────────────────────────
async function selectArchetype() {
    const archetypesDir = path.join(sourceDir, '.agent-os', 'templates', 'archetypes');
    if (!await fs.pathExists(archetypesDir)) return null;

    const archetypeFiles = await fs.readdir(archetypesDir);
    const archetypes = [];

    for (const file of archetypeFiles) {
        if (file.endsWith('.json')) {
            const data = await fs.readJson(path.join(archetypesDir, file));
            archetypes.push({ file, ...data });
        }
    }

    if (archetypes.length === 0) return null;

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

// ─── Selective Agent Copy (to global store) ─────────────────
async function copySelectedAgents(archetype, storePath) {
    const agentsSource = path.join(sourceDir, '.agent-os', 'agents');
    const agentsDest = path.join(storePath, '.agent-os', 'agents');

    // Always copy tier-1 (executive)
    const tier1Src = path.join(agentsSource, 'tier-1');
    const tier1Dest = path.join(agentsDest, 'tier-1');
    if (await fs.pathExists(tier1Src)) {
        await fs.copy(tier1Src, tier1Dest, { overwrite: true });
    }

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
        'marketing_growth': 'marketing-growth',
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

// ─── Selective Skills Copy (to global store) ────────────────
async function copySelectedSkills(archetype, storePath) {
    const skillsSource = path.join(sourceDir, '.agent-os', 'skills');
    const skillsDest = path.join(storePath, '.agent-os', 'skills');

    if (!archetype.requiredSkills) {
        await fs.copy(skillsSource, skillsDest, { overwrite: true });
        return;
    }

    const essentialFiles = ['doc.md', 'democracy-protocol.skill.md', 'memory-compression.skill.md'];
    for (const file of essentialFiles) {
        const src = path.join(skillsSource, file);
        const dest = path.join(skillsDest, file);
        if (await fs.pathExists(src)) {
            await fs.copy(src, dest, { overwrite: true });
        }
    }

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

// ─── Doctor Command ──────────────────────────────────────────
async function doctor() {
    console.log(pc.cyan('\n🩺 Running Agent-Kit Health Check (v2.0)...\n'));

    // Step 1: Check for .agentkit pointer
    let pointer = await readPointer(targetDir);
    const pointerPath = getPointerFilePath(targetDir);
    if (!fs.existsSync(pointerPath)) {
        console.log(pc.red(`  ❌ ${POINTER_FILENAME} pointer file not found.`));
        console.log(`  Run: ${pc.yellow('npx @ab_aswini/agent-kit-p1 init')}\n`);
        return;
    }

    pointer = await readPointer(targetDir); // Read pointer after checking existence

    console.log(pc.green(`  ✅ Pointer: .agentkit (v${pointer.version})`));
    console.log(pc.gray(`     Store: ${pointer.store}`));

    // Step 2: Validate global store
    let issues = 0;

    const required = [
        { key: 'agents', label: 'Agent Definitions' },
        { key: 'rules', label: 'Universal Rules' },
        { key: 'skills', label: 'Skills Library' },
        { key: 'memory', label: 'Memory Store' },
        { key: 'scripts', label: 'Utility Scripts' },
    ];

    for (const { key, label } of required) {
        const p = pointer.paths[key] ? pointer.paths[key].replace(/\//g, path.sep) : '';
        if (p && await fs.pathExists(p)) {
            console.log(pc.green(`  ✅ ${label}: OK`));
        } else {
            console.log(pc.red(`  ❌ ${label}: MISSING (${key})`));
            issues++;
        }
    }

    // Step 3: Check for leftover legacy files
    const legacyPaths = ['.agent-os', 'memory', 'scripts', 'docs', 'manifest.json', 'METADATA.md', 'PROJECT_STATUS.md'];
    const legacyFound = [];
    for (const lp of legacyPaths) {
        if (await fs.pathExists(path.join(targetDir, lp))) {
            legacyFound.push(lp);
        }
    }

    if (legacyFound.length > 0) {
        console.log(pc.yellow(`\n  ⚠️  Legacy footprint detected in project root:`));
        for (const lf of legacyFound) {
            console.log(pc.yellow(`     - ${lf}`));
        }
        console.log(pc.gray(`     Run: npx @ab_aswini/agent-kit-p1 clean`));
        issues++;
    }

    console.log('');
    if (issues === 0) {
        console.log(pc.green('✨ System is Healthy! Zero-footprint verified.'));
    } else {
        console.log(pc.yellow(`⚠️ Found ${issues} issue(s). See recommendations above.`));
    }
}

// ─── Clean Command ───────────────────────────────────────────
async function clean() {
    console.log(pc.cyan('\n🧹 Cleaning legacy Agent-Kit footprint from project...\n'));

    const legacyPaths = [
        '.agent-os',
        'memory',
        'scripts',
        'docs',
        'manifest.json',
        'METADATA.md',
        'PROJECT_STATUS.md',
    ];

    let cleaned = 0;
    for (const lp of legacyPaths) {
        const fullPath = path.join(targetDir, lp);
        if (await fs.pathExists(fullPath)) {
            const stat = await fs.stat(fullPath);
            if (stat.isDirectory()) {
                await fs.remove(fullPath);
            } else {
                await fs.unlink(fullPath);
            }
            console.log(pc.green(`  ✅ Removed: ${lp}`));
            cleaned++;
        }
    }

    if (cleaned === 0) {
        console.log(pc.gray('  Nothing to clean — project is already clean.'));
    } else {
        console.log(pc.green(`\n✨ Cleaned ${cleaned} legacy items.`));
        console.log(pc.gray('  Your project is now footprint-free.'));

        if (!await fs.pathExists(getPointerFilePath(targetDir))) {
            console.log(pc.yellow('\n  💡 Run: npx @ab_aswini/agent-kit-p1 init'));
            console.log(pc.gray('     To re-initialize with the new isolated store.'));
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

    console.log(pc.cyan('🚀 Initializing Agent-Kit v2.0 (Isolated Mode)...\n'));

    try {
        // 1. Compute global store path
        const storePath = getGlobalStorePath(targetDir);
        await fs.ensureDir(storePath);

        console.log(pc.gray(`  📦 Global store: ${storePath}`));

        if (archetype) {
            // ── SELECTIVE MODE ──
            const coreFolders = ['rules', 'configs', 'config', 'templates', 'workflows', 'logs', 'scripts', '.shared'];
            for (const folder of coreFolders) {
                const src = path.join(sourceDir, '.agent-os', folder);
                const dest = path.join(storePath, '.agent-os', folder);
                if (await fs.pathExists(src)) {
                    await fs.copy(src, dest, { overwrite: true });
                }
            }

            const hubSrc = path.join(sourceDir, '.agent-os', 'hub-logic.md');
            const hubDest = path.join(storePath, '.agent-os', 'hub-logic.md');
            if (await fs.pathExists(hubSrc)) {
                await fs.copy(hubSrc, hubDest, { overwrite: true });
            }

            await copySelectedAgents(archetype, storePath);
            await copySelectedSkills(archetype, storePath);

            const topFolders = ['docs', 'memory', 'scripts'];
            for (const folder of topFolders) {
                const src = path.join(sourceDir, folder);
                const dest = path.join(storePath, folder);
                if (await fs.pathExists(src)) {
                    console.log(pc.gray(`  Syncing ${folder}...`));
                    await fs.copy(src, dest, { overwrite: true });
                }
            }
        } else {
            // ── FULL MODE ──
            const foldersToCopy = ['.agent-os', 'docs', 'memory', 'scripts'];
            for (const folder of foldersToCopy) {
                const src = path.join(sourceDir, folder);
                const dest = path.join(storePath, folder);
                if (await fs.pathExists(src)) {
                    console.log(pc.gray(`  Syncing ${folder}...`));
                    await fs.copy(src, dest, { overwrite: true, errorOnExist: false });
                }
            }
        }

        // 2. Copy metadata to global store (NOT to user project)
        const filesToCopy = ['manifest.json', 'METADATA.md', 'PROJECT_STATUS.md'];
        for (const file of filesToCopy) {
            const src = path.join(sourceDir, file);
            const dest = path.join(storePath, file);
            if (await fs.pathExists(src)) {
                await fs.copy(src, dest, { overwrite: true });
            }
        }

        // 3. Write .agentkit pointer (ONLY file we touch in user's project)
        const pointerConfig = buildPointerConfig(targetDir, storePath);
        const pointerPath = getPointerFilePath(targetDir);
        await fs.writeJson(pointerPath, pointerConfig, { spaces: 4 });

        console.log(pc.green(`\n  ✅ Pointer written: ${POINTER_FILENAME}`));

        const agentCount = archetype ? archetype.agents.length : 53;
        console.log(pc.green(`\n✅ Agent-Kit v2.0 initialized! (${agentCount} agents deployed)`));
        console.log(pc.white('\n🛡️  Zero-Footprint Mode Active'));
        console.log(pc.gray('  Your project stays clean — all agent infrastructure'));
        console.log(pc.gray(`  lives in: ${storePath}\n`));
        console.log(pc.white('Next steps:'));
        console.log(pc.gray('  1. Open the project in your AI-powered IDE.'));
        console.log(pc.gray('  2. Run "npx @ab_aswini/agent-kit-p1 doctor" to verify.'));
        console.log(pc.gray('  3. Instruct your AI to read .agentkit for path resolution.'));
        console.log(pc.gray(`  4. Add "${POINTER_FILENAME}" to your .gitignore.\n`));

        if (archetype) {
            console.log(pc.gray(`  💡 Archetype: ${archetype.name}`));
            console.log(pc.gray(`  📦 To switch to full fleet later: npx @ab_aswini/agent-kit-p1 init`));
        }
    } catch (err) {
        console.error(pc.red('\n❌ Error during initialization:'), err.message);
        process.exit(1);
    }
}

// ─── Interactive Chat Interceptor (REPL) ─────────────────────
async function startChatRepl() {
    console.log(pc.cyan('\n💬 Agent-Kit Interactive REPL'));
    console.log(pc.gray('   Type /help to see all commands. Type "exit" to quit.\n'));

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
        prompt: pc.green('❯ ')
    });

    const dispatcher = new SlashDispatcher();

    // Custom prompt styling logic
    const updatePrompt = () => {
        const badge = dispatcher.getBadge();
        const icon = dispatcher.activeCommand ? '' : pc.green('❯ ');
        rl.setPrompt(`${badge} ${icon}`);
        rl.prompt();
    };

    updatePrompt();

    for await (const line of rl) {
        const input = line.trim();

        if (input.toLowerCase() === 'exit' || input.toLowerCase() === 'quit') {
            console.log(pc.cyan('Goodbye! 👋'));
            rl.close();
            process.exit(0);
        }

        if (input === '') {
            updatePrompt();
            continue;
        }

        // Parse input via dispatcher
        const parsedContext = dispatcher.parse(input);

        // Dispatch logic
        const routeInfo = dispatcher.dispatch(parsedContext);

        if (routeInfo) {
            // Processing animation / Loading State
            console.log(pc.dim('  ⚡ Routing to ' + pc.yellow(routeInfo.agentId) + '...'));

            // In a headless setup, we'll invoke the spawn_agent.py to get the resolved system prompt.
            // It will print the wrapped system prompt, giving the feel of the LLM receiving the payload.

            try {
                // Find python path via pointer resolution (spawn_agent handles this internally now)
                const spawnScriptPath = path.join(sourceDir, 'scripts', 'spawn_agent.py');

                // Construct shell execution
                const pythonProcess = spawn('python', [spawnScriptPath, routeInfo.agentId], {
                    stdio: ['ignore', 'pipe', 'pipe']
                });

                let buffer = '';
                pythonProcess.stdout.on('data', (data) => buffer += data.toString());
                pythonProcess.stderr.on('data', (data) => console.log(pc.red(data.toString())));

                await new Promise((resolve) => pythonProcess.on('close', resolve));

                // Print the injected result block
                console.log(`\n${routeInfo.badgeColor('┌── System Prompt Injected ────────────────────')}`);
                console.log(pc.gray(routeInfo.injectedPrompt.substring(0, 150) + '...'));
                console.log(routeInfo.badgeColor('└─────────────────────────────────────────────\n'));

                console.log(pc.green('✅ Payload ready. (To use with an LLM, pipe this via API.)\n'));

            } catch (err) {
                console.log(pc.red('❌ Error invoking agent spawn logic:\n' + err));
            }

            // Reset after one-shot command execution
            dispatcher.reset();
        }

        updatePrompt();
    }
}

// ─── Command Router ──────────────────────────────────────────
if (command === 'doctor') {
    doctor();
} else if (command === 'clean') {
    clean();
} else if (command === 'chat') {
    startChatRepl();
} else if (command === 'run') {
    const taskPrompt = args.slice(1).join(' ');
    if (!taskPrompt) {
        console.log(pc.red('Error: The "run" command requires a task prompt.'));
        console.log(pc.yellow('Usage: npx @ab_aswini/agent-kit-p1 run "build a login page"'));
        process.exit(1);
    }
    require('./engine.js')(taskPrompt);
} else if (command === 'sync') {
    const watchMode = args.includes('--watch') || args.includes('-w');
    const scriptPath = path.join(sourceDir, 'scripts', 'memory_sync.py');
    const syncArgs = ['--path', targetDir];
    if (watchMode) syncArgs.push('--watch');
    console.log(pc.cyan('\n🧠 Agent-Kit Semantic Memory Sync' + (watchMode ? ' (Watch Mode)' : '') + '\n'));
    const { spawnSync } = require('child_process');
    spawnSync('python', [scriptPath, ...syncArgs], { stdio: 'inherit', cwd: targetDir });
} else if (command === 'mcp') {
    require('./mcp.js');
} else if (command === 'init' || !command) {
    init();
} else {
    console.log(pc.yellow(`Unknown command: ${command}`));
    console.log('Available commands: init, doctor, clean, chat, run, sync, mcp');
    console.log('Usage: npx @ab_aswini/agent-kit-p1 init');
    console.log('       npx @ab_aswini/agent-kit-p1 init --interactive');
    console.log('       npx @ab_aswini/agent-kit-p1 doctor');
    console.log('       npx @ab_aswini/agent-kit-p1 clean');
    console.log('       npx @ab_aswini/agent-kit-p1 chat');
    console.log('       npx @ab_aswini/agent-kit-p1 run "prompt"');
    console.log('       npx @ab_aswini/agent-kit-p1 sync');
    console.log('       npx @ab_aswini/agent-kit-p1 sync --watch');
    console.log('       npx @ab_aswini/agent-kit-p1 mcp');
}
