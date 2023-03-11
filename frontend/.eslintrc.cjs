module.exports = {
  extends: [
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier',
    'plugin:@typescript-eslint/recommended-requiring-type-checking'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    tsconfigRootDir: __dirname,
    project: ['./tsconfig.json']
  },
  plugins: ['@typescript-eslint', 'react', '@blueprintjs'],
  root: true,
  rules: {
  'react/prop-types': 'off',
  'react/react-in-jsx-scope': 'off',
  '@typescript-eslint/no-unsafe-member-access': 'off'
  },
};
