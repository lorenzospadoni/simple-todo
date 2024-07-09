import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';

export default {
  input: 'src/index.js', // Adjust the input file path as needed
  output: {
    file: 'dist/draggable.bundle.js',
    format: 'es', // ES module format
  },
  plugins: [resolve(), commonjs()],
};