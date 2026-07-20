export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
}

export interface Resource {
  id: number;
  resource_type: string;
  name: string;
  cloud_id: string;
  region: string;
  status: string;
  terraform_workspace: string;
  config_json: string;
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface Deployment {
  id: number;
  resource_id: number;
  github_repo: string;
  github_branch: string;
  docker_image: string;
  status: string;
  github_run_id: string;
  logs: string;
  deployed_by: number;
  created_at: string;
  updated_at: string;
}

export interface Repo {
  full_name: string;
  name: string;
  default_branch: string;
  html_url: string;
}

export interface Branch {
  name: string;
  commit_sha: string;
}

export interface InstanceMetrics {
  instance_id: string;
  cpu: { timestamp: string; value: number }[];
  memory: { timestamp: string; value: number }[];
  disk: { timestamp: string; value: number }[];
}

export interface ContainerInfo {
  id: string;
  name: string;
  status: string;
  image: string;
  created: string;
  ports: string;
}
