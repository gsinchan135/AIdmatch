import express from 'express';
import fs from 'fs';
import path from 'path';
import cors from 'cors';
import { fileURLToPath } from 'url';

const app = express();
const PORT = 3001;
app.use(cors({origin: "*"}));
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const donorsFilePath = path.join(__dirname, '../mock_db', 'Donors.json');

app.post('/donors', (req, res) => {
  const donor = req.body;
  
  fs.readFile(donorsFilePath, 'utf8', (readErr, data) => {
    if (readErr && readErr.code !== 'ENOENT') {
      return res.status(500).json({ error: 'Error reading donor file' });
    }

    let donors = [];
    if (data) {
      try {
        donors = JSON.parse(data);
      } catch (parseErr) {
        return res.status(500).json({ error: 'Error parsing donor file' });
      }
    }

    donors.push(donor);

    fs.writeFile(donorsFilePath, JSON.stringify(donors, null, 2), (writeErr) => {
      if (writeErr) {
        return res.status(500).json({ error: 'Error saving donor data' });
      }
      res.json({ message: 'Donor data saved successfully!' });
    });
  });

});

app.get('/donors', (req, res) => {
    fs.readFile(donorsFilePath, 'utf8', (readErr, data) => {
      if (readErr) return res.status(500).json({ error: 'Error reading donor file' });
      
      let donors = [];
      try {
        donors = JSON.parse(data);
      } catch (parseErr) {
        return res.status(500).json({ error: 'Error parsing donor file' });
      }
  
      res.json(donors);
    });
  });

  app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });