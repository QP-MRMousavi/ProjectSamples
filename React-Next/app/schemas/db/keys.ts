export type Keys = {
  id: number;
  user_id: number;
  key: string;
  level: number;
  ignore_limits: boolean;
  is_private_key: boolean;
  ip_addresses?: string | null;
  date_created: number;
};
