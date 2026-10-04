#!/usr/bin/env node
/**
 * Titan Zero Merge Validator - Phase 5
 * Validates recovery branches before integration
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function exec(cmd) {
  return execSync(cmd, {
    encoding: 'utf-8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function formatError(error) {
  return error.stderr?.toString().trim() || error.message;
}

function validateMerge(branch) {
  const result = {
    id: `validate-${Date.now()}`,
    branch,
    timestamp: new Date().toISOString(),
    checks: [],
    overall_status: 'pass',
    can_merge: true,
    issues: [],
  };

  console.log(`🔍 Validating merge for ${branch}...\n`);

  // Check 1: Branch exists
  try {
    exec(`git rev-parse --verify ${branch}`);
    result.checks.push({
      name: 'Branch exists',
      status: 'pass',
      message: `Branch ${branch} exists`,
    });
    console.log('  ✅ Branch exists');
  } catch {
    result.checks.push({
      name: 'Branch exists',
      status: 'fail',
      message: `Branch ${branch} not found`,
    });
    result.overall_status = 'fail';
    result.can_merge = false;
    result.issues.push('Branch does not exist');
    console.log('  ❌ Branch not found');
  }

  // Check 2: Builds successfully
  process.stdout.write('  Building...');
  try {
    exec(`git checkout ${branch}`);
    exec('npm run build');
    result.checks.push({
      name: 'Builds successfully',
      status: 'pass',
      message: 'Build completed without errors',
    });
    console.log(' ✅');
  } catch (err) {
    result.checks.push({
      name: 'Builds successfully',
      status: 'fail',
      message: formatError(err),
    });
    result.overall_status = 'fail';
    result.can_merge = false;
    result.issues.push('Build failed');
    console.log(' ❌');
  }

  // Check 3: Tests pass
  process.stdout.write('  Testing...');
  try {
    exec('npm test');
    result.checks.push({
      name: 'Tests pass',
      status: 'pass',
      message: 'All tests passed',
    });
    console.log(' ✅');
  } catch (err) {
    result.checks.push({
      name: 'Tests pass',
      status: 'warning',
      message: 'Some tests failed - review needed',
    });
    result.overall_status = 'warning';
    result.issues.push('Test failures detected');
    console.log(' ⚠️');
  }

  // Check 4: Duplicate detection is not implemented by this script.
  process.stdout.write('  Checking duplicates...');
  result.checks.push({
    name: 'No duplicate classes',
    status: 'not_run',
    message: 'No duplicate-class scanner is wired into this validator.',
  });
  result.overall_status = 'warning';
  result.can_merge = false;
  result.issues.push('Duplicate-class check not run');
  console.log(' ⚠️');

  // Check 5: Import validation is not implemented by this script.
  process.stdout.write('  Validating imports...');
  result.checks.push({
    name: 'All imports valid',
    status: 'not_run',
    message: 'No import-resolution check is wired into this validator.',
  });
  result.overall_status = 'warning';
  result.can_merge = false;
  result.issues.push('Import-resolution check not run');
  console.log(' ⚠️');

  // Check 6: This is an ancestry check, not a full merge-conflict check.
  process.stdout.write('  Checking branch ancestry...');
  try {
    exec(`git merge-base --is-ancestor main ${branch}`);
    result.checks.push({
      name: 'Branch contains main',
      status: 'pass',
      message: 'The branch contains the current main history.',
    });
    console.log(' ✅');
  } catch {
    result.checks.push({
      name: 'Branch contains main',
      status: 'warning',
      message: 'The branch is not based on current main; review or rebase before merging.',
    });
    result.overall_status = 'warning';
    result.can_merge = false;
    result.issues.push('Branch ancestry requires review');
    console.log(' ⚠️');
  }

  // Check 7: Architecture validation is not implemented by this script.
  process.stdout.write('  Auditing architecture...');
  result.checks.push({
    name: 'Architecture valid',
    status: 'not_run',
    message: 'No DI, route, or migration audit is wired into this validator.',
  });
  result.overall_status = 'warning';
  result.can_merge = false;
  result.issues.push('Architecture audit not run');
  console.log(' ⚠️');

  return result;
}

function writeValidationResult(result) {
  const auditDir = path.join(__dirname, '../audits');
  const resultPath = path.join(auditDir, `validation-${result.branch}.json`);

  if (!fs.existsSync(auditDir)) {
    fs.mkdirSync(auditDir, { recursive: true });
  }

  fs.writeFileSync(resultPath, JSON.stringify(result, null, 2));
  console.log(`\n✅ Validation result saved to ${resultPath}`);
}

function printResult(result) {
  console.log('\n📋 Validation Results');
  console.log('====================');
  console.log(`Branch: ${result.branch}`);
  console.log(`Overall Status: ${result.overall_status}`);
  console.log(`Can Merge: ${result.can_merge ? '✅ YES' : '❌ NO'}`);

  console.log('\nChecks:');
  for (const check of result.checks) {
    const icon = check.status === 'pass' ? '✅' : check.status === 'warning' || check.status === 'not_run' ? '⚠️' : '❌';
    console.log(`  ${icon} ${check.name}`);
    console.log(`     ${check.message}`);
  }

  if (result.issues.length > 0) {
    console.log('\nIssues:');
    for (const issue of result.issues) {
      console.log(`  - ${issue}`);
    }
  }
}

async function main() {
  const branch = process.argv[2];

  if (!branch) {
    console.error('Usage: validate-merge.js <branch-name>');
    process.exit(1);
  }

  try {
    const result = validateMerge(branch);
    writeValidationResult(result);
    printResult(result);
    process.exit(result.can_merge ? 0 : 1);
  } catch (error) {
    console.error('❌ Validation failed:', error.message);
    process.exit(1);
  }
}

main();
