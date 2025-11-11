import { useState } from "react";
import { api } from "../lib/api";
import {
  Box, Paper, Typography, TextField, Button, Stack, Alert, LinearProgress,
} from "@mui/material";

export default function Upload() {
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const upload = async () => {
    if (!title.trim() || !file) return;
    setBusy(true);
    setMsg("");
    try {
      const form = new FormData();
      form.append("file", file);
      // title is query param in your backend
      await api.post(`/upload_meeting?title=${encodeURIComponent(title)}`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMsg("Uploaded & processed successfully.");
      setTitle("");
      setFile(null);
    } catch (e) {
      setMsg("Upload failed. Check backend logs.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ maxWidth: 700, mx: "auto" }}>
        <Paper elevation={0} sx={{ p: 3, borderRadius: 3, border: "1px solid #e5e7eb", bgcolor: "white" }}>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>Upload Meeting Transcript</Typography>

          <Stack spacing={2}>
            <TextField
              label="Meeting title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              fullWidth
            />
            <Button variant="outlined" component="label">
              {file ? file.name : "Choose .txt transcript"}
              <input type="file" hidden accept=".txt,.md" onChange={(e) => setFile(e.target.files[0])} />
            </Button>

            {busy && <LinearProgress />}

            <Button variant="contained" onClick={upload} disabled={!title.trim() || !file || busy}>
              Upload & Process
            </Button>

            {!!msg && <Alert severity={msg.includes("success") ? "success" : "error"}>{msg}</Alert>}
          </Stack>
        </Paper>
      </Box>
    </Box>
  );
}
