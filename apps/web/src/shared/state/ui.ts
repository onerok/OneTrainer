import { TAB_IDS, type TabId } from '../../app/routes';

export type TabBooleanState = Record<TabId, boolean>;
export type TabStringState = Record<TabId, string>;

export function createTabBooleanState(initialValue: boolean): TabBooleanState {
  return TAB_IDS.reduce(
    (state, tabId) => {
      state[tabId] = initialValue;
      return state;
    },
    {} as TabBooleanState
  );
}

export function createTabStringState(initialValue: string): TabStringState {
  return TAB_IDS.reduce(
    (state, tabId) => {
      state[tabId] = initialValue;
      return state;
    },
    {} as TabStringState
  );
}
