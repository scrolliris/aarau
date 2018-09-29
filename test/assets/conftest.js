import path from 'path';

const project_root = (v) => {
  return path.resolve(__dirname, '..', '..', 'aarau', 'assets', v);
}

exports = { project_root };
