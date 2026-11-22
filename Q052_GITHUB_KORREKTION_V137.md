# Q052 · Korrigeret GitHub-overlevering for V137

V137 dokumenterede, at det lokale miljø afviste debuggeradgang før CLASS-start. Det var en teknisk status for den lokale kørsel. Jim uploader filerne til GitHub og starter beregningen manuelt. Det separate workflow nedenfor bruger GitHub-runneren til at afprøve V136-målingen af skalarfeltets interne start.

## Manuel upload til Morfindien/Bubbleverse

| Fil | Placering på standardbranchen |
|---|---|
| q052-scalar-start-v137.yml | .github/workflows/q052-scalar-start-v137.yml |
| Q052_STARTOBSERVATOER_V136.zip | Q052_STARTOBSERVATOER_V136.zip ved repository-roden |

Gem de to filer på standardbranchen. På GitHub under **Actions** vælges **Q052 V137 - Scalar startup on GitHub**. Klik **Run workflow** én gang. Det eksisterende workflow til V36 har sit eget formål og indeholder ikke denne startmåling.

## Resultat fra GitHub

Start med at hente artefaktet **q052-v137-github-result-[run-id]** fra kørslen. Det indeholder debuggerens testlog, byggeoplysninger, de to startkvitteringer og den uafhængige kontrol, når de er produceret. Hvis GitHub-runneren afviser hardware-breakpoints, stopper jobbet før CLASS og gemmer den tilgængelige log. Eventuelle rådata leveres som særskilte **q052-v137-github-raw-[del]-[run-id]** artefakter på højst 18 MB før GitHubs indpakning. De udpak­kede measured-filer samles i rækkefølge efter delnummer til én gzip-komprimeret tar-fil. Resultatartefaktet er tilstrækkeligt til første indtag.

Workflowet bruger det historiske CLASS-bibliotek fra V136, genbygger den arkiverede V69-observatør med de fastlagte compilerflag og genbruger begge oprindelige punktfiler. Den nye observerbinær får sit eget SHA-256-fingeraftryk. Kørslens GitHub-id og forsøgsnummer identificerer målingen. De nye målinger sammenholdes med V69 via de gemte eksporthashes.

## Verifikationsstatus

GitHub-projekthukommelsen er læst ved commit 147b5921488b0d63580bcc0b57748b226b5e35fd. V36-workflowet på den commit bruger manuel start på ubuntu-24.04 med det fastlåste CLASS-kildecommit. Den nye workflowfil er kontrolleret lokalt som YAML, og dens Bash- og indlejrede Python-kode er syntakskontrolleret. V136-arkivet er verificeret efter udpakning. GDB, kompileringen på GitHub-runneren og det nominelle par afprøves ved den manuelle GitHub-kørsel.

Dette tillæg retter V137's køreplan. Det lokale afslag fra V137 registreres som historisk. Hvis GitHub-runneren består testen, er dens måling næste input til Resultatindtag og routing 2.3.0 for Q052. Ved en konkret GitHub-fejl kan indtagsmotoren vurdere V137's forslag om direkte registrering i CLASS-koden. Pointtotalen for det hidtidige arbejde er 15.978. Der mangler 22 point til næste SoMe-pakke.
