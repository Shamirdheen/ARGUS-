import { OpeningEye } from "@/components/brand/RiskEye";

/** Shown inside the app shell while a route segment loads (Next.js loading.js convention). */
export default function Loading() {
  return (
    <div className="min-h-[50vh] grid place-items-center">
      <OpeningEye />
    </div>
  );
}
