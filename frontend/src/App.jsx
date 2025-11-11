import { Routes, Route, Link, useLocation } from "react-router-dom";
import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material";
import Upload from "./pages/Upload.jsx";
import Ask from "./pages/Ask.jsx";
import MeetingDetails from "./pages/MeetingDetails.jsx";

export default function App() {
  const location = useLocation();
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f5f7fb" }}>
      <AppBar position="sticky" elevation={0} sx={{ bgcolor: "#171A21" }}>
        <Toolbar sx={{ gap: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            Smart Meeting Agent
          </Typography>
          <Box sx={{ flex: 1 }} />
          <Button component={Link} to="/upload" color="inherit" variant={location.pathname==="/upload"?"outlined":"text"}>
            Upload
          </Button>
          <Button component={Link} to="/ask" color="inherit" variant={location.pathname==="/ask"?"outlined":"text"}>
            Ask
          </Button>
        </Toolbar>
      </AppBar>

      <Routes>
        <Route path="/" element={<Ask />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/ask" element={<Ask />} />
        <Route path="/meeting/:title" element={<MeetingDetails />} />
      </Routes>
    </Box>
  );
}
