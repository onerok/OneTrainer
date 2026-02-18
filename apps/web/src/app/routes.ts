export type AppRoute = {
  id: string;
  label: string;
  disabled: boolean;
};

export const TAB_ROUTES: AppRoute[] = [
  { id: 'general', label: 'General', disabled: false },
  { id: 'model', label: 'Model', disabled: false },
  { id: 'lora', label: 'LoRA', disabled: false },
  { id: 'data', label: 'Data', disabled: false },
  { id: 'concepts', label: 'Concepts', disabled: false },
  { id: 'training', label: 'Training', disabled: false },
  { id: 'sampling', label: 'Sampling', disabled: false },
  { id: 'backup', label: 'Backup', disabled: false },
  { id: 'tools', label: 'Tools', disabled: false }
];
