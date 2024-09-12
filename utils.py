import { spawn } from 'child_process';
import * as fs from 'fs';

const runPY = () => {
  const pythonProcess = spawn('python', ['-W', 'ignore', '/path/to/tip_workflow.py']);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python script exited with code ${code}`);
    if (code === 0) {
      // Process success, proceed with file reading
      fs.readFile('table.txt', 'utf8', (err, data) => {
        if (err) {
          console.error(err);
          return;
        }
        console.log(data);
      });
    } else {
      console.error('Python script failed.');
    }
  });
};

runPY();