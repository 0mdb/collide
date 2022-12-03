module.exports = {
  extends: [
    'plugin:@typescript-eslint/recommended',
    'plugin:@blueprintjs/recommended',
    'plugin:react/recommended',
    'prettier',
    'airbnb-typescript',
    'plugin:@typescript-eslint/recommended-requiring-type-checking'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    tsconfigRootDir: __dirname,
    project: ['./tsconfig.json']
  },
  plugins: ['@typescript-eslint', 'react', '@blueprintjs'],
  root: true,
  // rules: {
  // 'react/prop-types': 'off',
  // 'react/restructuring-assignment': 'off',
  // 'prefer-template': 'off',
  // 'react/jsx-filename-extension': [
  //   1,
  //   {
  //     extensions: ['.ts', '.tsx'],
  //   },
  // ],
  // },
};
