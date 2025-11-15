import { useEffect, useRef, useState } from "react";
import {
  Box,
  Paper,
  Stack,
  TextField,
  IconButton,
  Typography,
  Avatar,
  CircularProgress,
  Alert,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import { api } from "../lib/api";

export default function Chat({ meeting }) {
  const [messages, setMessages] = useState([
    { role: "bot", content: "Ask anything about this meeting." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const endRef = useRef(null);

  const scrollDown = () => {
    setTimeout(() => {
      endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  useEffect(scrollDown, [messages, loading]);

  const send = async () => {
    if (!input.trim() || !meeting) return;

    setError("");

    const userMsg = { role: "user", content: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const { data } = await api.post("/ask", {
        meeting,
        query: userMsg.content,
      });

      const botMsg = {
        role: "bot",
        content: data?.response || "No response available.",
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: "Server error. Please try again.",
        },
      ]);
      setError("Failed to contact backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", p: 2 }}>
      <Paper
        elevation={0}
        sx={{
          p: 2,
          minHeight: "60vh",
          bgcolor: "white",
          borderRadius: 3,
          border: "1px solid #e5e7eb",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {error && <Alert severity="error">{error}</Alert>}

        <Stack spacing={2} sx={{ flex: 1, overflowY: "auto" }}>
          {messages.map((m, i) => (
            <Box
              key={i}
              sx={{
                display: "flex",
                justifyContent: m.role === "user" ? "flex-end" : "flex-start",
                alignItems: "flex-start",
                gap: 1,
              }}
            >
              {m.role === "bot" && (
                <Avatar sx={{ bgcolor: "#6d28d9", width: 32, height: 32 }}>
                  <AutoAwesomeIcon fontSize="small" />
                </Avatar>
              )}
              <Paper
                elevation={0}
                sx={{
                  px: 2,
                  py: 1.25,
                  borderRadius:
                    m.role === "user"
                      ? "18px 18px 4px 18px"
                      : "18px 18px 18px 4px",
                  bgcolor: m.role === "user" ? "#4f46e5" : "#f8fafc",
                  color: m.role === "user" ? "white" : "inherit",
                  maxWidth: "75%",
                  border: m.role === "user" ? "none" : "1px solid #e5e7eb",
                }}
              >
                <Typography sx={{ whiteSpace: "pre-wrap" }}>
                  {m.content}
                </Typography>
              </Paper>
            </Box>
          ))}

          {loading && (
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <Avatar sx={{ bgcolor: "#6d28d9", width: 32, height: 32 }}>
                <AutoAwesomeIcon fontSize="small" />
              </Avatar>
              <CircularProgress size={22} />
            </Box>
          )}
          <div ref={endRef} />
        </Stack>

        <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            placeholder={
              meeting ? "Ask about this meeting..." : "Select a meeting first"
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
          />
          <IconButton
            onClick={send}
            disabled={!meeting || !input.trim() || loading}
            sx={{
              bgcolor: "#4f46e5",
              color: "white",
              "&:hover": { bgcolor: "#4338ca" },
            }}
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Paper>
    </Box>
  );
}
