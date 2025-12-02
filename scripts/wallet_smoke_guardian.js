/**
 * 🛡️ Wallet Smoke Guardian - Playwright Smoke Test
 * 
 * This script performs smoke tests on the Pi Forge wallet integration
 * and captures comprehensive diagnostic artifacts on failure or exit:
 * - Full page screenshots at major steps
 * - HAR file containing network requests
 * - Console log file capturing console.* messages and errors
 * - Playwright trace (.zip) for deep debugging
 * 
 * All artifacts are written to ./logs/ with 'smoke-' prefix.
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Configuration
const LOGS_DIR = path.join(process.cwd(), 'logs');
const TEST_URL = process.env.SMOKE_TEST_URL || 'http://localhost:8000';
const TIMESTAMP = new Date().toISOString().replace(/[:.]/g, '-');
const IS_CI = process.env.CI === 'true';

// Warn if using default URL in CI
if (!process.env.SMOKE_TEST_URL && IS_CI) {
  console.warn('⚠️ SMOKE_TEST_URL not set - using default localhost:8000');
  console.warn('   Set the SMOKE_TEST_URL repository variable for production testing');
}

// Artifact paths with smoke- prefix
const ARTIFACTS = {
  screenshot: {
    connect: path.join(LOGS_DIR, `smoke-screenshot-connect-${TIMESTAMP}.png`),
    confirmation: path.join(LOGS_DIR, `smoke-screenshot-confirmation-${TIMESTAMP}.png`),
    success: path.join(LOGS_DIR, `smoke-screenshot-success-${TIMESTAMP}.png`),
    error: path.join(LOGS_DIR, `smoke-screenshot-error-${TIMESTAMP}.png`),
  },
  har: path.join(LOGS_DIR, `smoke-network-${TIMESTAMP}.har`),
  console: path.join(LOGS_DIR, `smoke-console-${TIMESTAMP}.log`),
  trace: path.join(LOGS_DIR, `smoke-trace-${TIMESTAMP}.zip`),
};

// Console log collector
const consoleLogs = [];

/**
 * Ensure logs directory exists
 */
function ensureLogsDir() {
  if (!fs.existsSync(LOGS_DIR)) {
    fs.mkdirSync(LOGS_DIR, { recursive: true });
  }
}

/**
 * Write console logs to file
 */
function writeConsoleLogs() {
  const logContent = consoleLogs.map(entry => {
    const timestamp = new Date(entry.timestamp).toISOString();
    return `[${timestamp}] [${entry.type.toUpperCase()}] ${entry.text}`;
  }).join('\n');
  
  fs.writeFileSync(ARTIFACTS.console, logContent || 'No console messages captured.');
  console.log(`📝 Console log saved: ${ARTIFACTS.console}`);
}

/**
 * Capture screenshot with error handling
 */
async function captureScreenshot(page, name) {
  try {
    const screenshotPath = ARTIFACTS.screenshot[name];
    await page.screenshot({ 
      path: screenshotPath, 
      fullPage: true,
      timeout: 10000
    });
    console.log(`📸 Screenshot saved: ${screenshotPath}`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to capture ${name} screenshot:`, error.message);
    return false;
  }
}

/**
 * Main smoke test function
 */
async function runSmokeTest() {
  ensureLogsDir();
  
  let browser = null;
  let context = null;
  let page = null;
  let testPassed = false;

  console.log('🛡️ Wallet Smoke Guardian - Starting smoke test');
  console.log(`🌐 Target URL: ${TEST_URL}`);
  console.log(`📁 Artifacts directory: ${LOGS_DIR}`);
  console.log(`⏰ Timestamp: ${TIMESTAMP}`);
  console.log('═'.repeat(60));

  try {
    // Launch browser
    browser = await chromium.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    // Create context with HAR recording and tracing
    context = await browser.newContext({
      recordHar: {
        path: ARTIFACTS.har,
        mode: 'full',
        content: 'attach'
      },
      viewport: { width: 1280, height: 720 }
    });

    // Start tracing
    await context.tracing.start({
      screenshots: true,
      snapshots: true,
      sources: true
    });

    // Create page and attach console listener
    page = await context.newPage();
    
    // Capture all console messages
    page.on('console', msg => {
      consoleLogs.push({
        timestamp: Date.now(),
        type: msg.type(),
        text: msg.text()
      });
    });

    // Capture page errors
    page.on('pageerror', error => {
      consoleLogs.push({
        timestamp: Date.now(),
        type: 'error',
        text: `Page Error: ${error.message}`
      });
    });

    // Capture request failures
    page.on('requestfailed', request => {
      consoleLogs.push({
        timestamp: Date.now(),
        type: 'warning',
        text: `Request Failed: ${request.url()} - ${request.failure()?.errorText || 'Unknown error'}`
      });
    });

    // ============================================
    // STEP 1: Navigate to connect page
    // ============================================
    console.log('\n📍 Step 1: Navigating to connect page...');
    
    const response = await page.goto(TEST_URL, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });

    if (!response || !response.ok()) {
      throw new Error(`Failed to load page: ${response?.status() || 'No response'}`);
    }

    console.log(`✅ Page loaded: ${response.status()}`);
    await captureScreenshot(page, 'connect');

    // ============================================
    // STEP 2: Check for critical elements
    // ============================================
    console.log('\n📍 Step 2: Checking for critical page elements...');

    // Wait for body to be visible
    await page.waitForSelector('body', { timeout: 10000 });
    
    // Check page title exists
    const title = await page.title();
    console.log(`📄 Page title: ${title}`);

    // Check for common Pi Forge elements (adjust selectors as needed)
    const hasContent = await page.evaluate(() => {
      return document.body.innerText.length > 0;
    });

    if (!hasContent) {
      throw new Error('Page appears to be empty');
    }

    console.log('✅ Page has content');
    await captureScreenshot(page, 'confirmation');

    // ============================================
    // STEP 3: Verify page health indicators
    // ============================================
    console.log('\n📍 Step 3: Verifying page health...');

    // Check for JavaScript errors in console
    const jsErrors = consoleLogs.filter(log => log.type === 'error');
    if (jsErrors.length > 0) {
      console.warn(`⚠️ Found ${jsErrors.length} JavaScript error(s) in console`);
      jsErrors.forEach(err => console.warn(`   - ${err.text}`));
    }

    // Check for failed network requests
    const failedRequests = consoleLogs.filter(log => 
      log.type === 'warning' && log.text.startsWith('Request Failed:')
    );
    if (failedRequests.length > 0) {
      console.warn(`⚠️ Found ${failedRequests.length} failed network request(s)`);
    }

    // Final success screenshot
    await captureScreenshot(page, 'success');

    // ============================================
    // SMOKE TEST PASSED
    // ============================================
    console.log('\n═'.repeat(60));
    console.log('🎉 Wallet Smoke Test PASSED');
    testPassed = true;

  } catch (error) {
    // ============================================
    // SMOKE TEST FAILED
    // ============================================
    console.error('\n═'.repeat(60));
    console.error('❌ Wallet Smoke Test FAILED');
    console.error(`Error: ${error.message}`);
    
    // Capture error state screenshot
    if (page) {
      await captureScreenshot(page, 'error');
    }

  } finally {
    // ============================================
    // CLEANUP & ARTIFACT COLLECTION
    // ============================================
    console.log('\n📦 Collecting diagnostic artifacts...');

    // Write console logs
    writeConsoleLogs();

    // Stop tracing and save
    if (context) {
      try {
        await context.tracing.stop({ path: ARTIFACTS.trace });
        console.log(`🔍 Trace saved: ${ARTIFACTS.trace}`);
      } catch (traceError) {
        console.error(`❌ Failed to save trace: ${traceError.message}`);
      }
    }

    // Close context to flush HAR
    if (context) {
      try {
        await context.close();
        console.log(`🌐 HAR saved: ${ARTIFACTS.har}`);
      } catch (contextError) {
        console.error(`❌ Failed to close context: ${contextError.message}`);
      }
    }

    // Close browser
    if (browser) {
      await browser.close();
    }

    // List all generated artifacts
    console.log('\n📋 Generated Artifacts:');
    for (const [category, pathOrObj] of Object.entries(ARTIFACTS)) {
      if (typeof pathOrObj === 'string') {
        const exists = fs.existsSync(pathOrObj);
        const size = exists ? fs.statSync(pathOrObj).size : 0;
        console.log(`   ${exists ? '✓' : '✗'} ${path.basename(pathOrObj)} ${exists ? `(${formatBytes(size)})` : ''}`);
      } else {
        for (const [name, screenshotPath] of Object.entries(pathOrObj)) {
          const exists = fs.existsSync(screenshotPath);
          const size = exists ? fs.statSync(screenshotPath).size : 0;
          console.log(`   ${exists ? '✓' : '✗'} ${path.basename(screenshotPath)} ${exists ? `(${formatBytes(size)})` : ''}`);
        }
      }
    }

    // Exit with appropriate code
    if (!testPassed) {
      console.log('\n❌ Exiting with failure status');
      process.exit(1);
    }
    
    console.log('\n✅ Smoke test completed successfully');
  }
}

/**
 * Format bytes to human readable
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Run the smoke test
runSmokeTest().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
