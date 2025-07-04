// Configuration for the Redwood Digital University Calendar Frontend
// This file can be dynamically configured in containerized environments

window.ENV = window.ENV || {};

// Default configuration
const config = {
  // API Configuration
  CALENDAR_API_URL: window.ENV.REACT_APP_CALENDAR_API_URL || process.env.REACT_APP_CALENDAR_API_URL || 'http://127.0.0.1:8000',
  
  // Application Configuration
  APP_NAME: window.ENV.REACT_APP_NAME || process.env.REACT_APP_NAME || 'Redwood Digital University Calendar',
  APP_VERSION: window.ENV.REACT_APP_VERSION || process.env.REACT_APP_VERSION || '1.0.0',
  
  // University Branding
  UNIVERSITY_NAME: window.ENV.REACT_APP_UNIVERSITY_NAME || process.env.REACT_APP_UNIVERSITY_NAME || 'Redwood Digital University',
  SYSTEM_BRANDING: window.ENV.REACT_APP_SYSTEM_BRANDING || process.env.REACT_APP_SYSTEM_BRANDING || 'Powered by CanopyAI',
  
  // Feature Flags
  ENABLE_DELETE: window.ENV.REACT_APP_ENABLE_DELETE !== 'false',
  ENABLE_EDIT: window.ENV.REACT_APP_ENABLE_EDIT !== 'false',
  ENABLE_CREATE: window.ENV.REACT_APP_ENABLE_CREATE !== 'false',
  
  // UI Configuration
  DEFAULT_VIEW: window.ENV.REACT_APP_DEFAULT_VIEW || process.env.REACT_APP_DEFAULT_VIEW || 'month',
  THEME: window.ENV.REACT_APP_THEME || process.env.REACT_APP_THEME || 'default',
  
  // Debug Configuration
  DEBUG: window.ENV.REACT_APP_DEBUG === 'true' || process.env.REACT_APP_DEBUG === 'true' || false,
};

// Validate required configuration
if (!config.CALENDAR_API_URL) {
  console.error('❌ CALENDAR_API_URL is required but not configured');
}

// Log configuration in debug mode
if (config.DEBUG) {
  console.log('🔧 Calendar Frontend Configuration:', config);
}

export default config;