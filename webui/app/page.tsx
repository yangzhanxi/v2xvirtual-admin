import type { Metadata } from "next";

import LicensesManagement from '@/app/licenses/page'

export default function IndexPage() {
    return <LicensesManagement/>
}

export const metadata: Metadata = {
  title: "V2X Virtual Admin",
};
