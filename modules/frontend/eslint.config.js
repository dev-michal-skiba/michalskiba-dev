import eslint from '@eslint/js';
import noUnsanitized from 'eslint-plugin-no-unsanitized';
import html from 'eslint-plugin-html';
import globals from 'globals';

export default [
  {
    files: ["**/*.html", "**/*.js"],
    plugins: {
      'no-unsanitized': noUnsanitized,
      'html': html,
      'globals': globals,
    },
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'script',
      globals: {
        "bootstrap": true,
        ...globals.browser,
      }
    },
    rules: {
      'no-unsanitized/method': 'error',
      'no-unsanitized/property': 'error',
      ...eslint.configs.recommended.rules,
    },
  },
];
