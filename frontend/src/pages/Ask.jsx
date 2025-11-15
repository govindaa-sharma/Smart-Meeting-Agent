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
  Alert,
  CircularProgress,
} from "@mui/material";
import Chat from "../components/Chat.jsx";
import { Link } from "react-router-dom";

export default function Ask() {
  const [meetings, setMeetings] = useState([]);
  const [selected, setSelected] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState("");

  const loadMeetings = async () => {
    setLoading(true);
    setLoadError("");
    try {
      const { data } = await api.get("/meetings");
      setMeetings(data || []);
      if (data?.length && !selected) {
        setSelected(data[0]);
      }
    } catch {
      setLoadError("Couldn't load meeting list.");
      setMeetings([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMeetings();
  }, []);

  useEffect(() => {
    const refresh = localStorage.getItem("refreshMeetings");
    if (refresh) {
      loadMeetings();
      localStorage.removeItem("refreshMeetings");
    }
  }, []);

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ maxWidth: 900, mx: "auto", mb: 2 }}>
        <Paper
          elevation={0}
          sx={{
            p: 2,
            borderRadius: 3,
            border: "1px solid #e5e7eb",
            bgcolor: "white",
          }}
        >
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
            Saved Meetings
          </Typography>

          {loadError && <Alert severity="error">{loadError}</Alert>}
          {loading && <CircularProgress size={24} />}

          <FormControl fullWidth sx={{ mt: 1 }}>
            <InputLabel id="meet-label">Select Meeting</InputLabel>
            <Select
              labelId="meet-label"
              value={selected}
              label="Select Meeting"
              onChange={(e) => setSelected(e.target.value)}
            >
              {meetings.map((m) => (
                <MenuItem key={m} value={m}>
                  {m}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <Box sx={{ mt: 2, display: "flex", gap: 1 }}>
            {selected && (
              <Button component={Link} to={`/meeting/${selected}`} size="small">
                View summary
              </Button>
            )}
            <Button component={Link} to="/upload" size="small">
              Upload new
            </Button>
          </Box>
        </Paper>
      </Box>

      <Divider sx={{ maxWidth: 900, mx: "auto", my: 2 }} />

      <Chat meeting={selected} />
    </Box>
  );
}
