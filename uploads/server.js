const express = require('express');
const multer = require('multer');
const { Octokit } = require('@octokit/rest');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();
const uploadDir = 'uploads';

// Tạo thư mục uploads
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Middleware
app.use('/uploads', express.static(uploadDir));
app.use(express.static('public'));
app.use(express.json());

const OWNER = "sangdev27";
const REPO = "upfile";
const BRANCH = "main";

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

// Multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, uploadDir),
    filename: (req, file, cb) => cb(null, file.originalname)
});

const upload = multer({ storage: storage });

// ====================== UPLOAD ROUTE ======================
app.post('/upload', upload.array('files'), async (req, res) => {
    try {
        const { folder = 'uploads' } = req.body;
        const files = req.files;

        if (!files || files.length === 0) {
            return res.status(400).json({ success: false, error: "Không có file nào" });
        }

        const results = [];

        for (const file of files) {
            const filePath = `${folder}/${file.originalname}`;

            await octokit.repos.createOrUpdateFileContents({
                owner: OWNER,
                repo: REPO,
                path: filePath,
                message: `📤 Upload ${file.originalname}`,
                content: fs.readFileSync(file.path).toString('base64'),
                branch: BRANCH
            });

            const publicUrl = `https://upfile-laylien.onrender.com/uploads/${file.originalname}`;

            results.push({
                name: file.originalname,
                publicUrl: publicUrl
            });
        }

        res.json({
            success: true,
            message: `✅ Upload thành công ${files.length} file!`,
            files: results
        });

    } catch (error) {
        console.error("Lỗi:", error.message);
        res.status(500).json({
            success: false,
            error: "Lỗi khi upload file. Kiểm tra token hoặc tên repository."
        });
    }
});

// ====================== FRONTEND ROUTES ======================
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Catch-all route (sửa lỗi wildcard *)
app.use((req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
// ============================================================

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`🚀 Server chạy tại: http://localhost:${PORT}`);
    console.log(`🌐 Public: https://upfile-laylien.onrender.com`);
    console.log(`📁 Repo: ${OWNER}/${REPO}`);
});