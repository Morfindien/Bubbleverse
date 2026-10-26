# Q052 V2 — installation og næste kørsel

V2 er lokalt testet med 13 beståede tests. Den originale CLASS-binærfil er gendannet med præcis den fastlåste SHA-256. Ingen ny native beregning er kørt, og GitHub er ikke ændret i denne omgang.

1. Åbn [fillisten](sandbox:/workspace/scratch/0feff3e57b36/Q052_NATIVEPAIR_V2/FILES_Q052_NATIVEPAIR_V2.md) og download alle 15 installationsfiler.
2. Upload `.github/workflows/q052-native-pair-v2.yml` og `.github/workflows/q052-install-nativepair-v2.yml` til netop `.github/workflows/`. Upload de øvrige installationsfiler til repositoryets rod, herunder `Q052_ORIGINAL_CLASSY_PINNED.so` og det gendannede Q048-checkpoint.
3. Gem filerne på `main`. Bevar V1-filerne og den permanente `00-bubbleverse-start.yml`.
4. Åbn GitHub Actions og kør **Install Q052 native pair V2** én gang. Den kontrollerer alle filhashes og den forventede registry/README-base. Kun den nye registry-post og en README-indledning ændres. Hvis basen er ændret, stopper den med en præcis fejl; brug ikke en tvungen overskrivning.
5. Efter en vellykket installation: åbn **🚀 BUBBLEVERSE START**, indtast **Q052-NATIVEPAIR-V2**, og kør én gang.
6. Send `Q052_NATIVEPAIR_RESULT_V2.json`, `Q052_UPSTREAM_JOBS_V2.json` og de rå grenartefakter tilbage til **Result Ingestion & Routing 2.3.0**, uanset om beregningen lykkes eller stopper.

Den oprindelige binærfil medleveres som en enkelt fil på cirka 9 MB. Fysikkernen bygges ikke om. Native-jobbet bruger Python 3.11.16 og checker den oprindelige kildekode ud på det fastlåste commit. V2 gemmer også en læsbar JSON ved manglende grene og fejl før beregningen.

Registryets `Q-052` er den eksplicitte stavemåde, som START-launcheren kræver. Det videnskabelige spørgsmål hedder stadig **Q052**.

Q052 står på **800 point**. Der er ingen SoMe-pakke forfalden. De analytiske Q051-grænser er ikke målte native forskelle, og to præcisionsniveauer giver ikke i sig selv det krævede rigorøse fejlcertifikat.

Journal V4, ledger V4, handoff V4, proveniens og testlog ligger separat i fillisten. De kan uploades som projektets hukommelse sammen med programfilerne. V4-journalen indeholder hele V1–V3 uændret plus den nye post.
