import { useEffect, useState } from "react";
import { api } from "../lib/api";
import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Button,
} from "@mui/material";
import Chat from "../components/Chat.jsx";
import { Link } from "react-router-dom";

export default function Ask() {
  const [meetings, setMeetings] = useState([]);
  const [selected, setSelected] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/meetings");
        setMeetings(data || []);
        if ((data || []).length && !selected) setSelected(data[0]);
      } catch {
        setMeetings([]);
      }
    })();
  }, []);

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ maxWidth: 900, mx: "auto", mb: 2 }}>
        <Paper elevation={0} sx={{ p: 2, borderRadius: 3, border: "1px solid #e5e7eb", bgcolor: "white" }}>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 700 }}>
            Saved Meetings
          </Typography>

          <FormControl fullWidth>
            <InputLabel id="meet-label">Select meeting</InputLabel>
            <Select
              labelId="meet-label"
              label="Select meeting"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              {meetings.map((m) => (
                <MenuItem key={m} value={m}>{m}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ mt: 1, display: "flex", gap: 1 }}>
            {selected && (
              <Button
                component={Link}
                to={`/meeting/${encodeURIComponent(selected)}`}
                size="small"
              >
                View summary & actions
              </Button>
            )}
            <Button component={Link} to="/upload" size="small">
              Upload new meeting
            </Button>
          </Box>
        </Paper>
      </Box>

      <Divider sx={{ maxWidth: 900, mx: "auto", mb: 2 }} />

      <Chat meeting={selected} />
    </Box>
  );
}
