import { BANK_JSON } from "./bank-data";

export type Item = {
  id: string;
  category: string;
  standard: string;
  type: "MC" | "MS";
  dok: number;
  calculator: string;
  stem: string;
  choices: string[];
  answer: number[];
  explanation: string;
  rationales: string[];
  errors: (string | null)[];
  template: string;
};
export type Bank = {
  items: Item[];
  errorTypes: Record<string, string>;
  standardList: { code: string; name: string; cat: string }[];
  categories: Record<string, string>;
};

export const BANK: Bank = JSON.parse(BANK_JSON);
export const ITEMS: Map<string, Item> = new Map(BANK.items.map(i => [i.id, i]));
export const baseStandard = (s: string) => s.split(".").slice(0, 5).join(".");

/** What a student may see before answering: no keys, explanations or error tags. */
export function studentBank() {
  return {
    standardList: BANK.standardList,
    categories: BANK.categories,
    items: BANK.items.map(i => ({
      id: i.id, category: i.category, standard: i.standard, type: i.type, dok: i.dok,
      calculator: i.calculator, stem: i.stem, choices: i.choices,
    })),
  };
}

export function staffBank() {
  return {
    standardList: BANK.standardList,
    categories: BANK.categories,
    errorTypes: BANK.errorTypes,
    items: BANK.items.map(({ template, ...rest }) => rest),
  };
}

export function grade(item: Item, picked: number[]) {
  const pick = [...new Set(picked)].filter(n => Number.isInteger(n) && n >= 0 && n < item.choices.length).sort();
  const correct = pick.length === item.answer.length && item.answer.every(a => pick.includes(a));
  const err = !correct && item.type === "MC" && pick.length === 1 ? item.errors[pick[0]] ?? null : null;
  return { pick, correct, err };
}
