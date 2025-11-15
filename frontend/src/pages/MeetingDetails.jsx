import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../lib/api";
import {
  Box,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
  Alert,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

export default function MeetingDetails() {
  const { title } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      setErr("");
      try {
        const { data } = await api.get(`/meeting/${encodeURIComponent(title)}`);
        setData(data);
      } catch {
        setErr("Could not load meeting details.");
      } finally {
        setLoading(false);
      }
    })();
  }, [title]);

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ maxWidth: 900, mx: "auto" }}>
        <Paper
          elevation={0}
          sx={{
            p: 3,
            borderRadius: 3,
            border: "1px solid #e5e7eb",
            bgcolor: "white",
          }}
        >
          {loading && <CircularProgress />}
          {err && <Alert severity="error">{err}</Alert>}

          {data && (
            <>
              <Typography variant="h5" sx={{ fontWeight: 800, mb: 1 }}>
                {data.title}
              </Typography>

              <Typography variant="subtitle2" sx={{ color: "text.secondary" }}>
                Summary
              </Typography>
              <Typography sx={{ whiteSpace: "pre-wrap", mt: 1 }}>
                {data.summary || "No summary available."}
              </Typography>

              <Divider sx={{ my: 3 }} />

              <Typography variant="subtitle2" sx={{ color: "text.secondary" }}>
                Action Items
              </Typography>

              <List dense>
                {(data.actions || []).length === 0 && (
                  <Typography sx={{ mt: 1 }}>No action items.</Typography>
                )}

                {(data.actions || []).map((a, idx) => (
                  <ListItem key={idx} disablePadding sx={{ py: 0.5 }}>
                    <ListItemIcon>
                      <CheckCircleIcon sx={{ color: "#16a34a" }} />
                    </ListItemIcon>
                    <ListItemText primary={a} />
                  </ListItem>
                ))}
              </List>
            </>
          )}
        </Paper>
      </Box>
    </Box>
  );
}
