# Candidatures assistées par Claude

Objectif : envoyer **plusieurs candidatures de qualité par jour** en laissant Claude faire le travail répétitif (tri des offres, lettres, emails), tout en gardant **toi** comme validateur final.

> ⚠️ Pourquoi pas 100 % automatique ? LinkedIn, Indeed, Welcome to the Jungle, etc. interdisent les robots qui postulent à ta place : ton compte peut être bloqué. Et les recruteurs repèrent vite les candidatures envoyées en masse. La bonne méthode, c'est que Claude prépare tout et que tu valides chaque envoi en un clic (≈ 1 min par candidature au lieu de 30).

---

## Niveau 1 : dans le chat Claude (claude.ai), sans code

1. Crée un **Projet** sur claude.ai et mets dans ses connaissances : ton CV + `profil.md` (rempli).
2. Ajoute ces **instructions du projet** :
   ```
   Pour chaque offre que je colle : donne un score d'adéquation /100, les points forts,
   les manques, puis une lettre de motivation (250-350 mots) et un email court.
   N'invente jamais d'expérience. Écris en français.
   ```
3. Chaque jour, colle 5 à 10 offres → copie, relis, envoie.
4. Si le connecteur **Gmail** est activé, demande : « crée un brouillon Gmail pour chaque offre au-dessus de 70 ». Il ne te reste qu'à relire et cliquer sur Envoyer.

## Niveau 2 : le script Python de ce dossier (API Claude)

```bash
cd candidatures-claude
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # clé sur console.anthropic.com
# 1. remplis profil.md
# 2. colle chaque offre dans offres/nom-entreprise.txt (URL + texte de l'offre)
python generer.py --min-score 60
```

Résultat dans `sortie/AAAA-MM-JJ/` :
- `resume.json` : offres triées par score,
- `<offre>.json` : score, points forts, manques, objet + corps de l'email,
- `<offre>-lettre.md` : lettre de motivation prête à relire.

Coût indicatif : quelques centimes par offre.

## Niveau 3 : routine quotidienne avec Claude Code (le plus « expert »)

Claude Code peut lancer une **routine planifiée** (ex. tous les jours à 8 h) qui :
1. cherche les nouvelles offres sur le web selon tes critères,
2. les enregistre dans `offres/`,
3. lance l'analyse et rédige les candidatures,
4. crée des **brouillons Gmail** (jamais d'envoi automatique),
5. te laisse un résumé.

Prompt de routine à utiliser (demande à Claude Code : « crée une routine quotidienne à 8 h avec ce prompt ») :

```
Lis candidatures-claude/profil.md. Cherche sur le web les offres publiées ces dernières
24 h correspondant à mes intitulés, lieux et contrats (sites carrières des entreprises,
Indeed, Welcome to the Jungle, Emploi.ci…). Ignore celles déjà présentes dans
candidatures-claude/suivi.csv. Pour les 10 meilleures : enregistre le texte dans offres/,
évalue l'adéquation, rédige lettre + email, et crée un BROUILLON Gmail (ne jamais envoyer)
pour celles avec un score ≥ 70 et un email de contact. Ajoute une ligne par offre dans
suivi.csv (date, entreprise, poste, url, score, statut=brouillon). Termine par un résumé.
```

Ensuite, chaque matin : ouvre Gmail → Brouillons → relis → Envoyer.

---

## Conseils d'expert

- **La qualité du profil fait tout.** Des réalisations chiffrées dans `profil.md` = des lettres crédibles.
- **Filtre avant de postuler** : mieux vaut 5 candidatures à 80/100 que 30 à 40/100.
- **Relis toujours** : nom de l'entreprise, poste, ton. Claude peut se tromper.
- **Fais un suivi** (`suivi.csv`) pour relancer au bout de 7-10 jours. Claude peut aussi rédiger les relances.
- **Adapte aussi le CV** : demande « réordonne mon CV pour cette offre » pour les offres > 85.
