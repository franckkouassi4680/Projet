"""Prépare des candidatures personnalisées avec Claude.

Pour chaque offre dans offres/*.txt, Claude :
  1. évalue l'adéquation avec profil.md (score 0-100),
  2. rédige une lettre de motivation et un email de candidature adaptés.

Rien n'est envoyé automatiquement : les résultats sont écrits dans sortie/
pour que tu les relises avant d'envoyer (ou de créer un brouillon Gmail).

Usage :
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python generer.py               # traite toutes les offres
    python generer.py --min-score 60
"""

import argparse
import json
from datetime import date
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

ICI = Path(__file__).parent
MODELE = "claude-opus-5-5"

SYSTEME = """Tu es un conseiller en recrutement francophone. On te donne le profil
d'un candidat et une offre d'emploi. Tu dois :
- évaluer honnêtement l'adéquation (score 0-100) et lister les points forts / manques ;
- rédiger une lettre de motivation courte (250-350 mots), concrète, sans formules creuses,
  qui reprend le vocabulaire de l'offre et cite des réalisations réelles du profil ;
- rédiger un email de candidature bref (objet + corps de 5-8 lignes).
N'invente JAMAIS une compétence, un diplôme ou une expérience absente du profil.
Si une exigence de l'offre n'est pas couverte, mentionne-la dans `manques`, pas dans la lettre."""


class Candidature(BaseModel):
    entreprise: str
    poste: str
    contact_email: str | None = Field(description="Email de candidature trouvé dans l'offre, sinon null")
    score: int = Field(description="Adéquation profil/offre de 0 à 100")
    points_forts: list[str]
    manques: list[str]
    lettre_motivation: str
    email_objet: str
    email_corps: str


def preparer(client: anthropic.Anthropic, profil: str, offre: str) -> Candidature | None:
    reponse = client.beta.messages.parse(
        model=MODELE,
        max_tokens=16000,
        system=SYSTEME,
        output_config={"effort": "medium"},
        # Si le modèle refuse la requête, l'API la relance sur un modèle de secours.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[{
            "role": "user",
            "content": f"<profil>\n{profil}\n</profil>\n\n<offre>\n{offre}\n</offre>",
        }],
        output_format=Candidature,
    )
    if reponse.stop_reason == "refusal":
        return None
    return reponse.parsed_output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-score", type=int, default=0, help="ignore les offres sous ce score")
    args = parser.parse_args()

    profil = (ICI / "profil.md").read_text(encoding="utf-8")
    offres = sorted((ICI / "offres").glob("*.txt"))
    if not offres:
        print("Aucune offre dans offres/ — colle le texte de chaque offre dans un fichier .txt")
        return

    sortie = ICI / "sortie" / date.today().isoformat()
    sortie.mkdir(parents=True, exist_ok=True)
    client = anthropic.Anthropic()

    resume = []
    for chemin in offres:
        print(f"→ {chemin.name} ...", end=" ", flush=True)
        try:
            c = preparer(client, profil, chemin.read_text(encoding="utf-8"))
        except anthropic.APIError as e:
            print(f"erreur API : {e}")
            continue
        if c is None:
            print("refusé par le modèle, ignoré")
            continue
        print(f"score {c.score}")
        resume.append({"fichier": chemin.name, "entreprise": c.entreprise, "poste": c.poste, "score": c.score})
        if c.score < args.min_score:
            continue
        (sortie / f"{chemin.stem}.json").write_text(
            json.dumps(c.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (sortie / f"{chemin.stem}-lettre.md").write_text(c.lettre_motivation, encoding="utf-8")

    resume.sort(key=lambda r: r["score"], reverse=True)
    (sortie / "resume.json").write_text(json.dumps(resume, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nRésultats dans {sortie} (triés par score dans resume.json). Relis avant d'envoyer !")


if __name__ == "__main__":
    main()
