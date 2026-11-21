import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  Bell,
  CheckCircle2,
  ChevronDown,
  Clock3,
  Database,
  FileSearch,
  Fingerprint,
  GitBranch,
  LayoutDashboard,
  Network,
  Search,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Terminal,
  UserX,
} from "lucide-react";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import "./App.css";

import {
  fetchStatistics,
  fetchInvestigations,
  fetchInvestigationDetails,
  fetchCorrelations,
} from "./services/api";

const activityData = [
  { time: "09:00", events: 12 },
  { time: "10:00", events: 18 },
  { time: "11:00", events: 14 },
  { time: "12:00", events: 25 },
  { time: "13:00", events: 19 },
  { time: "14:00", events: 32 },
  { time: "15:00", events: 22 },
  { time: "16:00", events: 28 },
  { time: "17:00", events: 16 },
];


const navigation = [
  {
    section: "WORKSPACE",
    items: [
      { label: "Overview", icon: LayoutDashboard, active: true },
      { label: "Investigations", icon: FileSearch },
      { label: "Evidence Timeline", icon: Clock3 },
      { label: "Correlations", icon: GitBranch },
      { label: "Knowledge Graph", icon: Network },
    ],
  },
  {
    section: "SYSTEM",
    items: [
      { label: "Evidence Sources", icon: Database },
      { label: "Audit & Activity", icon: Activity },
    ],
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <Fingerprint size={23} />
        </div>
        <div>
          <h2>FORENSIQ</h2>
          <span>DIGITAL FORENSICS</span>
        </div>
      </div>

      <div className="workspace-selector">
        <div className="workspace-icon">
          <Shield size={18} />
        </div>
        <div className="workspace-text">
          <span>WORKSPACE</span>
          <strong>Forensic Lab</strong>
        </div>
        <ChevronDown size={15} />
      </div>

      <nav className="navigation">
        {navigation.map((group) => (
          <div className="nav-group" key={group.section}>
            <p className="nav-heading">{group.section}</p>

            {group.items.map((item) => {
              const Icon = item.icon;

              return (
                <button
                  className={`nav-item ${item.active ? "active" : ""}`}
                  key={item.label}
                  type="button"
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                  {item.label === "Investigations" && (
                    <span className="nav-count">3</span>
                  )}
                </button>
              );
            })}
          </div>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <div className="system-status">
          <span className="status-dot" />
          <div>
            <strong>System operational</strong>
            <span>Neo4j connected</span>
          </div>
        </div>

        <div className="profile">
          <div className="avatar">IA</div>
          <div className="profile-info">
            <strong>Investigator</strong>
            <span>Administrator</span>
          </div>
          <ChevronDown size={16} />
        </div>
      </div>
    </aside>
  );
}

function Header() {
  return (
    <header className="topbar">
      <div className="breadcrumb">
        <span>Workspace</span>
        <span className="breadcrumb-divider">/</span>
        <strong>Overview</strong>
      </div>

      <div className="topbar-actions">
        <div className="environment-badge">
          <span className="status-dot" />
          LOCAL ENVIRONMENT
        </div>

        <button className="icon-button" aria-label="Search" type="button">
          <Search size={19} />
        </button>

        <button className="icon-button notification-button" aria-label="Notifications" type="button">
          <Bell size={19} />
          <span />
        </button>

        <div className="topbar-avatar">IA</div>
      </div>
    </header>
  );
}

function StatCard({ title, value, subtitle, icon: Icon, accent, trend }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{title}</span>
        <div className={`stat-icon ${accent}`}>
          <Icon size={19} />
        </div>
      </div>

      <div className="stat-value">{value}</div>

      <div className="stat-bottom">
        <span className="stat-subtitle">{subtitle}</span>
        {trend && (
          <span className="stat-trend">
            <ArrowUpRight size={14} />
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}

function ActivityPanel() {
  return (
    <section className="panel activity-panel">
      <div className="panel-header">
        <div>
          <h3>Evidence Activity</h3>
          <p>Illustrative event activity throughout the day</p>
        </div>

        <button className="period-button" type="button">
          Today <ChevronDown size={14} />
        </button>
      </div>

      <div className="chart-legend">
        <span className="legend-dot" />
        Evidence events
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={activityData}
            margin={{ top: 12, right: 8, left: -18, bottom: 0 }}
          >
            <defs>
              <linearGradient id="eventGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.24} />
                <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
              </linearGradient>
            </defs>

            <CartesianGrid
              stroke="#263344"
              strokeDasharray="4 5"
              vertical={false}
            />

            <XAxis
              dataKey="time"
              stroke="#718096"
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#8291a5", fontSize: 11 }}
            />

            <YAxis
              stroke="#718096"
              tickLine={false}
              axisLine={false}
              tick={{ fill: "#8291a5", fontSize: 11 }}
            />

            <Tooltip
              contentStyle={{
                background: "#111c2b",
                border: "1px solid #29384a",
                borderRadius: "9px",
                color: "#e2e8f0",
              }}
              labelStyle={{ color: "#94a3b8" }}
            />

            <Area
              type="monotone"
              dataKey="events"
              stroke="#22d3ee"
              strokeWidth={2.5}
              fill="url(#eventGradient)"
              activeDot={{ r: 5, fill: "#22d3ee" }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

function AssessmentPanel({ statistics }) {
  const total = statistics?.total_investigations ?? 0;
  const requires = statistics?.requires_investigation ?? 0;
  const correlated = statistics?.correlated_activity_observed ?? 0;
  const neutral = statistics?.no_significant_finding ?? 0;

  const percentage = (value) =>
    total > 0 ? `${(value / total) * 100}%` : "0%";

  return (
    <section className="panel assessment-panel">
      <div className="panel-header">
        <div>
          <h3>Investigation Assessment</h3>
          <p>Current sequence classifications</p>
        </div>
      </div>

      <div className="assessment-summary">
        <div className="assessment-number">{total}</div>
        <span>Total investigations</span>
      </div>

      <div className="assessment-item">
        <div className="assessment-label">
          <span className="assessment-dot suspicious-dot" />
          <span>Requires investigation</span>
          <strong>{requires}</strong>
        </div>
        <div className="progress-track">
          <div className="progress-fill suspicious-fill"
            style={{ width: percentage(requires) }} />
        </div>
      </div>

      <div className="assessment-item">
        <div className="assessment-label">
          <span className="assessment-dot normal-dot" />
          <span>Correlated activity</span>
          <strong>{correlated}</strong>
        </div>
        <div className="progress-track">
          <div className="progress-fill correlated-fill"
            style={{ width: percentage(correlated) }} />
        </div>
      </div>

      <div className="assessment-item">
        <div className="assessment-label">
          <span className="assessment-dot neutral-dot" />
          <span>No significant finding</span>
          <strong>{neutral}</strong>
        </div>
        <div className="progress-track">
          <div className="progress-fill neutral-fill"
            style={{ width: percentage(neutral) }} />
        </div>
      </div>

      <div className="assessment-note">
        <ShieldCheck size={16} />
        Classifications are based on hybrid analysis.
      </div>
    </section>
  );
}

function InvestigationTable({ investigations, loading, error, onSelect }) {
  return (
    <section className="panel table-panel">
      <div className="panel-header">
        <div>
          <h3>Recent Investigations</h3>
          <p>Forensic sequences generated from collected evidence</p>
        </div>

        <button className="view-all-button" type="button">
          View all <ArrowUpRight size={15} />
        </button>
      </div>

      <div className="table-scroll">
        <table className="investigation-table">
          <thead>
            <tr>
              <th>SEQUENCE</th>
              <th>USER</th>
              <th>SOURCE IP</th>
              <th>EVENTS</th>
              <th>ML PREDICTION</th>
              <th>SCORE</th>
              <th>ASSESSMENT</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
  <tr><td colSpan="7">Loading investigations...</td></tr>
) : error ? (
  <tr><td colSpan="7">{error}</td></tr>
) : investigations.map((item) => {
  const id = `SEQ-${String(item.sequence_id).padStart(3, "0")}`;
  const prediction =
    item.ml_prediction === "suspicious" ? "Suspicious" : "Normal";

  const status =
    item.assessment === "requires_investigation"
      ? "Requires Investigation"
      : item.assessment === "correlated_activity_observed"
        ? "Correlated Activity"
        : "No Significant Finding";

  const tagClass =
    item.assessment === "requires_investigation"
      ? "tag-suspicious"
      : item.assessment === "correlated_activity_observed"
        ? "tag-correlated"
        : "tag-neutral";

  return (
    <tr
  key={item.sequence_id}
  onClick={() => onSelect(item.sequence_id)}
  style={{ cursor: "pointer" }}
>
      <td><span className="sequence-id">{id}</span></td>
      <td>{item.user}</td>
      <td className="ip-cell">{item.source_ip || "—"}</td>
      <td>{item.event_count}</td>
      <td>
        <span className={`prediction ${
          prediction === "Suspicious"
            ? "prediction-suspicious"
            : "prediction-normal"
        }`}>
          {prediction === "Suspicious"
            ? <AlertTriangle size={13} />
            : <CheckCircle2 size={13} />}
          {prediction}
        </span>
      </td>
      <td className="score-cell">
        {Number(item.suspicious_score ?? 0).toFixed(2)}
      </td>
      <td>
        <span className={`assessment-tag ${tagClass}`}>
          {status}
        </span>
      </td>
    </tr>
  );
})}
          </tbody>
        </table>
      </div>

      <div className="table-footer">
        Showing 3 of 3 investigations
        <span>Data from forensic analysis pipeline</span>
      </div>
    </section>
  );
}
function InvestigationDetails({ sequenceId, onBack }) {
  const [details, setDetails] = useState(null);
  const [correlations, setCorrelations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadDetails() {
      try {
        setLoading(true);
        setError("");

        const [detailData, correlationData] = await Promise.all([
          fetchInvestigationDetails(sequenceId),
          fetchCorrelations(sequenceId),
        ]);

        if (!cancelled) {
          setDetails(detailData);
          setCorrelations(correlationData.correlations || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadDetails();

    return () => {
      cancelled = true;
    };
  }, [sequenceId]);

  const sequenceLabel = `SEQ-${String(sequenceId).padStart(3, "0")}`;

  if (loading) {
    return <section className="panel" style={{ padding: "24px" }}>
      Loading investigation details...
    </section>;
  }

  if (error) {
    return (
      <section className="panel" style={{ padding: "24px" }}>
        <p style={{ color: "#fb7777" }}>{error}</p>
        <button className="view-all-button" onClick={onBack}>
          Back to Overview
        </button>
      </section>
    );
  }

  if (!details) return null;

  const firstEvent = details.evidence_timeline?.[0] || {};
  const investigationUser = details.user || firstEvent.user || "Unknown";
  const investigationIP = details.source_ip || firstEvent.source_ip || "Unknown";

  const assessmentLabels = {
    requires_investigation: "Requires Investigation",
    correlated_activity_observed: "Correlated Activity Observed",
    no_significant_finding: "No Significant Finding",
  };

  return (
    <div className="investigation-details-page">
      <button
        className="view-all-button"
        type="button"
        onClick={onBack}
        style={{ marginBottom: "24px" }}
      >
        ← Back to Overview
      </button>

      <div className="page-heading">
        <div>
          <div className="eyebrow">
            <Terminal size={14} />
            DIGITAL FORENSICS / INVESTIGATION
          </div>
          <h1>{sequenceLabel}</h1>
          <p>Detailed forensic investigation and evidence analysis.</p>
        </div>
      </div>

      <section className="stats-grid">
        <StatCard
          title="ML Prediction"
          value={details.ml_prediction || "Unknown"}
          subtitle="Sequence classification"
          icon={ShieldAlert}
          accent="red"
        />

        <StatCard
          title="Suspicious Score"
          value={Number(details.suspicious_score ?? 0).toFixed(2)}
          subtitle="Model output score, not attack probability"
          icon={Activity}
          accent="purple"
        />

        <StatCard
          title="Evidence Events"
          value={details.evidence_timeline?.length ?? 0}
          subtitle="Events in this sequence"
          icon={Database}
          accent="blue"
        />

        <StatCard
          title="Correlations"
          value={correlations.length}
          subtitle="Linked evidence relationships"
          icon={GitBranch}
          accent="cyan"
        />
      </section>

      <section className="panel" style={{ padding: "24px", marginTop: "20px" }}>
        <h3>Investigation Assessment</h3>
        <p>{assessmentLabels[details.assessment] || details.assessment}</p>
      </section>

      <section
        className="panel"
        style={{
          padding: "24px",
          marginTop: "20px",
          display: "grid",
          gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
          gap: "24px",
        }}
      >
        <div>
          <span className="eyebrow">INVESTIGATION SUBJECT</span>
          <h3 style={{ marginTop: "10px" }}>{investigationUser}</h3>
        </div>

        <div>
          <span className="eyebrow">SOURCE IP ADDRESS</span>
          <h3 style={{ marginTop: "10px" }}>{investigationIP}</h3>
        </div>

        <div>
          <span className="eyebrow">INVESTIGATION ID</span>
          <h3 style={{ marginTop: "10px" }}>{sequenceLabel}</h3>
        </div>
      </section>

      <section className="panel" style={{ padding: "24px", marginTop: "20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "16px", marginBottom: "8px", flexWrap: "wrap" }}>
          <div>
            <h3 style={{ marginBottom: "6px" }}>Evidence Timeline</h3>
            <p style={{ margin: 0, color: "#8291a5", fontSize: "13px" }}>
              Chronological sequence of collected forensic events
            </p>
          </div>
          <span style={{ color: "#94a3b8", fontSize: "12px" }}>
            {details.evidence_timeline?.length ?? 0} EVENTS
          </span>
        </div>

        {details.evidence_timeline?.length ? (
          <div style={{ marginTop: "22px" }}>
            {details.evidence_timeline.map((event, index) => {
              const sourceName = String(event.source || "unknown").toLowerCase();
              const isAuth = sourceName.includes("auth");
              const isFirewall = sourceName.includes("firewall");
              const isBrowser = sourceName.includes("browser");
              const EventIcon = isAuth ? Fingerprint : isFirewall ? ShieldAlert : isBrowser ? Activity : Database;
              const sourceLabel = isAuth ? "AUTHENTICATION" : isFirewall ? "FIREWALL" : isBrowser ? "BROWSER HISTORY" : sourceName.replaceAll("_", " ").toUpperCase();
              const statusText = String(event.status || event.action || "recorded").toUpperCase();
              const isNegative = /fail|deny|blocked|reject|error/i.test(`${event.status || ""} ${event.action || ""}`);
              const statusColor = isNegative ? "#fb7777" : "#34d399";
              const statusBackground = isNegative ? "rgba(248, 113, 113, 0.12)" : "rgba(52, 211, 153, 0.12)";

              return (
                <div
                  key={`${event.position}-${index}`}
                  style={{ display: "grid", gridTemplateColumns: "34px minmax(0, 1fr)", columnGap: "16px", position: "relative", paddingBottom: index === details.evidence_timeline.length - 1 ? "0" : "24px" }}
                >
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", height: "100%" }}>
                    <div style={{ width: "34px", height: "34px", borderRadius: "10px", display: "grid", placeItems: "center", color: isNegative ? "#fb7777" : "#22d3ee", background: isNegative ? "rgba(248, 113, 113, 0.12)" : "rgba(34, 211, 238, 0.12)", border: "1px solid #29384a", zIndex: 1 }}>
                      <EventIcon size={17} />
                    </div>
                    {index !== details.evidence_timeline.length - 1 && (
                      <div style={{ width: "1px", flex: 1, minHeight: "100px", background: "#334155", marginTop: "6px" }} />
                    )}
                  </div>

                  <div style={{ background: "#0d1928", border: "1px solid #263648", borderRadius: "12px", padding: "16px 18px", minWidth: 0 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px", flexWrap: "wrap" }}>
                      <div>
                        <div style={{ color: "#22d3ee", fontSize: "10px", fontWeight: 700, letterSpacing: "1px", marginBottom: "7px" }}>{sourceLabel}</div>
                        <strong style={{ color: "#e2e8f0", fontSize: "14px" }}>{event.event_type || "Evidence event"}</strong>
                      </div>
                      <span style={{ color: "#94a3b8", fontSize: "12px", fontVariantNumeric: "tabular-nums" }}>{event.timestamp || "Timestamp unavailable"}</span>
                    </div>

                    <div style={{ display: "flex", flexWrap: "wrap", gap: "8px 18px", marginTop: "14px", color: "#a8b6c8", fontSize: "12px" }}>
                      <span>User: <strong style={{ color: "#e2e8f0" }}>{event.user || "Unknown"}</strong></span>
                      <span>Source IP: <strong style={{ color: "#e2e8f0" }}>{event.source_ip || "Unknown"}</strong></span>
                    </div>

                    <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", gap: "10px", marginTop: "13px" }}>
                      <span style={{ color: "#94a3b8", fontSize: "12px" }}>Action: {event.action || "—"}</span>
                      <span style={{ color: statusColor, background: statusBackground, borderRadius: "6px", padding: "4px 8px", fontSize: "10px", fontWeight: 700, letterSpacing: "0.5px" }}>{statusText}</span>
                    </div>

                    {event.resource && (
                      <div style={{ marginTop: "12px", paddingTop: "10px", borderTop: "1px solid #263648", color: "#94a3b8", fontSize: "12px", overflowWrap: "anywhere" }}>
                        Resource: <span style={{ color: "#cbd5e1" }}>{event.resource}</span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <p>No evidence timeline available.</p>
        )}
      </section>

      <section className="panel" style={{ padding: "24px", marginTop: "20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "12px", flexWrap: "wrap", marginBottom: "20px" }}>
          <div>
            <h3 style={{ marginBottom: "6px" }}>Correlated Evidence</h3>
            <p style={{ margin: 0, color: "#8291a5", fontSize: "13px" }}>
              Relationships identified between events in this sequence
            </p>
          </div>
          <span style={{ color: "#94a3b8", fontSize: "12px" }}>
            {correlations.length} {correlations.length === 1 ? "RELATIONSHIP" : "RELATIONSHIPS"}
          </span>
        </div>

        {correlations.length ? (
          <div style={{ display: "grid", gap: "18px" }}>
            {correlations.map((item, index) => {
              const earlierEvent = item.earlier_event || {};
              const laterEvent = item.later_event || {};
              const correlationIP = earlierEvent.source_ip || laterEvent.source_ip || investigationIP;
              const timeDifference = Number(item.time_difference_seconds);
              const formattedDifference = Number.isFinite(timeDifference)
                ? `${timeDifference} seconds`
                : "Not available";

              return (
                <div
                  key={`${item.rule || "correlation"}-${index}`}
                  style={{ background: "#0d1928", border: "1px solid #263648", borderRadius: "12px", padding: "18px" }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: "12px", flexWrap: "wrap", marginBottom: "16px" }}>
                    <strong style={{ color: "#e2e8f0", fontSize: "13px", overflowWrap: "anywhere" }}>
                      {String(item.rule || "Evidence correlation").replaceAll("_", " ")}
                    </strong>
                    <span style={{ color: "#fbbf24", background: "rgba(251, 191, 36, 0.10)", border: "1px solid rgba(251, 191, 36, 0.22)", borderRadius: "999px", padding: "5px 9px", fontSize: "10px", fontWeight: 700, letterSpacing: "0.4px" }}>
                      CORRELATION DETECTED
                    </span>
                  </div>

                  <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1fr) auto minmax(0, 1fr)", alignItems: "center", gap: "12px" }}>
                    <div style={{ minWidth: 0, background: "rgba(248, 113, 113, 0.07)", border: "1px solid rgba(248, 113, 113, 0.20)", borderRadius: "10px", padding: "14px" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#fb7777", marginBottom: "10px" }}>
                        <UserX size={17} />
                        <span style={{ fontSize: "10px", fontWeight: 700, letterSpacing: "0.7px" }}>EARLIER EVENT</span>
                      </div>
                      <strong style={{ display: "block", color: "#e2e8f0", fontSize: "14px", overflowWrap: "anywhere" }}>
                        {earlierEvent.event_type || "Unknown event"}
                      </strong>
                      <span style={{ display: "block", color: "#94a3b8", fontSize: "11px", marginTop: "7px" }}>
                        {earlierEvent.timestamp || "Timestamp unavailable"}
                      </span>
                    </div>

                    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "7px", minWidth: "76px" }}>
                      <span style={{ color: "#fbbf24", fontSize: "11px", fontWeight: 700, textAlign: "center" }}>{formattedDifference}</span>
                      <ArrowRight size={22} color="#94a3b8" />
                    </div>

                    <div style={{ minWidth: 0, background: "rgba(248, 113, 113, 0.07)", border: "1px solid rgba(248, 113, 113, 0.20)", borderRadius: "10px", padding: "14px" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#fb7777", marginBottom: "10px" }}>
                        <ShieldAlert size={17} />
                        <span style={{ fontSize: "10px", fontWeight: 700, letterSpacing: "0.7px" }}>LATER EVENT</span>
                      </div>
                      <strong style={{ display: "block", color: "#e2e8f0", fontSize: "14px", overflowWrap: "anywhere" }}>
                        {laterEvent.event_type || "Unknown event"}
                      </strong>
                      <span style={{ display: "block", color: "#94a3b8", fontSize: "11px", marginTop: "7px" }}>
                        {laterEvent.timestamp || "Timestamp unavailable"}
                      </span>
                    </div>
                  </div>

                  <div style={{ display: "flex", flexWrap: "wrap", gap: "8px 18px", marginTop: "16px", paddingTop: "13px", borderTop: "1px solid #263648", color: "#94a3b8", fontSize: "12px" }}>
                    <span>Shared source IP: <strong style={{ color: "#e2e8f0" }}>{correlationIP}</strong></span>
                  </div>
                  <p style={{ color: "#cbd5e1", fontSize: "13px", lineHeight: 1.6, margin: "13px 0 0" }}>
                    {item.explanation || "The analysis identified a relationship between these evidence events."}
                  </p>
                </div>
              );
            })}
          </div>
        ) : (
          <p>No correlated evidence found for this sequence.</p>
        )}
      </section>

      <section className="panel" style={{ padding: "24px", marginTop: "20px" }}>
        <h3>Explainable Rule Findings</h3>

        {details.rule_findings?.length ? (
          <ul>
            {details.rule_findings.map((finding, index) => (
              <li key={index} style={{ marginBottom: "12px" }}>
                {finding}
              </li>
            ))}
          </ul>
        ) : (
          <p>No rule-based findings recorded.</p>
        )}
      </section>
    </div>
  );
}

function App() {
  const [statistics, setStatistics] = useState(null);
  const [selectedSequenceId, setSelectedSequenceId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState("");

  const [investigations, setInvestigations] = useState([]);
  const [investigationsLoading, setInvestigationsLoading] = useState(true);
  const [investigationsError, setInvestigationsError] = useState("");

  useEffect(() => {
    async function loadStatistics() {
      try {
        const data = await fetchStatistics();
        setStatistics(data);
      } catch (error) {
        setApiError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadStatistics();
  }, []);

  useEffect(() => {
    async function loadInvestigations() {
      try {
        const data = await fetchInvestigations();
        setInvestigations(data.investigations || []);
      } catch (error) {
        setInvestigationsError(error.message);
      } finally {
        setInvestigationsLoading(false);
      }
    }

    loadInvestigations();
  }, []);

  const flaggedInvestigations = investigations.filter(
  (item) => item.assessment === "requires_investigation"
);

  return (
    <div className="app-shell">
      <Sidebar />

      <main className="main-area">
        <Header />

        <div className="dashboard-content"></div>
           <div className="dashboard-content">
  {selectedSequenceId ? (
    <InvestigationDetails
      sequenceId={selectedSequenceId}
      onBack={() => setSelectedSequenceId(null)}
    />
  ) : (
    <>
      
          <div className="page-heading">
            <div>
              <div className="eyebrow">
                <Terminal size={14} />
                DIGITAL FORENSICS / OVERVIEW
              </div>
              <h1>Investigation Overview</h1>
              <p>
                Monitor evidence, examine correlations and review forensic
                investigation findings.
              </p>
            </div>

            <div className="heading-date">
              <Clock3 size={15} />
              <span>Forensic analysis workspace</span>
            </div>
          </div>

          {flaggedInvestigations.length > 0 ? (
  <div className="alert-banner">
    <div className="alert-icon">
      <ShieldAlert size={19} />
    </div>

    <div className="alert-content">
      <strong>Investigation requires attention</strong>
      <span>
        {flaggedInvestigations.map(
          (item) =>
            `SEQ-${String(item.sequence_id).padStart(3, "0")}`
        ).join(", ")}
        {" "}has been flagged for further investigation.
      </span>
    </div>

    <span className="alert-count">
      {flaggedInvestigations.length} FLAGGED
    </span>
  </div>
) : (
  <div className="alert-banner">
    <div className="alert-icon">
      <ShieldCheck size={19} />
    </div>

    <div className="alert-content">
      <strong>No investigations require immediate attention</strong>
      <span>
        No sequences are currently classified as requiring investigation.
      </span>
    </div>

    <span className="alert-count">0 FLAGGED</span>
  </div>
)}

          <section className="stats-grid">
            <StatCard
              title="Total Investigations"
              value={statistics?.total_investigations ?? "--"}
              subtitle="Forensic sequences"
              icon={FileSearch}
              accent="cyan"
            />

            <StatCard
              title="Evidence Events"
              value={statistics?.total_evidence_events ?? "--"}
              subtitle="Collected and normalized"
              icon={Database}
              accent="blue"
            />

            <StatCard
              title="Evidence Correlations"
              value={statistics?.total_correlations ?? "--"}
              subtitle="Rule-based relationships"
              icon={GitBranch}
              accent="purple"
            />

            <StatCard
              title="Requires Investigation"
              value={statistics?.requires_investigation ?? "--"}
              subtitle="Needs investigator review"
              icon={AlertTriangle}
              accent="red"
            />
          </section>

          <section className="analytics-grid">
            <ActivityPanel />
            <AssessmentPanel statistics={statistics}/>
          </section>

          <InvestigationTable
  investigations={investigations}
  loading={investigationsLoading}
  error={investigationsError}
  onSelect={(id) => setSelectedSequenceId(id)}
/>

          <footer className="dashboard-footer">
            <div>
              <span className="footer-status" />
              FORENSIQ INVESTIGATION SYSTEM
            </div>
            <span>AI-Based Digital Forensics & Evidence Correlation</span>
            <span>Version 1.0.0</span>
          </footer>
            </>
)}
        </div>
      </main>
    </div>
  );
}

export default App;