
const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchStatistics() {
  const response = await fetch(`${API_BASE_URL}/statistics/`);

  if (!response.ok) {
    throw new Error("Failed to fetch investigation statistics");
  }

  return response.json();
}

export async function fetchInvestigations() {
  const response = await fetch(`${API_BASE_URL}/investigations/`);

  if (!response.ok) {
    throw new Error("Failed to fetch investigations");
  }

  return response.json();
}

export async function fetchInvestigationDetails(sequenceId) {
  const response = await fetch(
    `${API_BASE_URL}/investigations/${sequenceId}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch investigation details");
  }

  return response.json();
}

export async function fetchCorrelations(sequenceId) {
  const response = await fetch(
    `${API_BASE_URL}/investigations/${sequenceId}/correlations`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch investigation correlations");
  }

  return response.json();
}
