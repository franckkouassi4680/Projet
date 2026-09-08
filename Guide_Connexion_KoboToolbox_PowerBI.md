# Guide complet : Connecter KoboToolbox Humanitarian à Power BI

*Guide pas-à-pas pour débutant en analyse de données*

---

## 1. Comprendre les bases avant de commencer

### 1.1 Qu'est-ce que KoboToolbox Humanitarian ?

KoboToolbox est un outil de collecte de données très utilisé dans le secteur humanitaire (ONG, agences ONU, ONGs locales). Il existe deux serveurs principaux :

- **`kf.kobotoolbox.org`** : le serveur "classique" (communauté générale)
- **`kobo.humanitarianresponse.info`** : le serveur **Humanitarian**, réservé aux acteurs humanitaires (OCHA, clusters humanitaires, etc.)

C'est ce deuxième serveur que vous utilisez. Retenez bien son adresse, elle sera importante plus tard.

### 1.2 Comment vos données sont stockées

Quand vous créez un formulaire dans KoboToolbox et que des enquêteurs le remplissent sur le terrain (via l'app KoboCollect ou en ligne), chaque réponse devient une **ligne de données** stockée sur le serveur KoboToolbox. Power BI ne va pas "voler" ces données : il va simplement s'y **connecter** pour les lire et les actualiser régulièrement.

### 1.3 Les 3 grandes méthodes de connexion

| Méthode | Niveau | Actualisation automatique | Recommandé pour |
|---|---|---|---|
| **Export manuel (XLSX/CSV)** | Débutant | ❌ Non (il faut réexporter à chaque fois) | Tester une fois, rapport ponctuel |
| **API REST de KoboToolbox (via Power Query)** | Intermédiaire | ✅ Oui | Usage recommandé pour la majorité des cas |
| **Connecteur OData** | Intermédiaire/Avancé | ✅ Oui, très stable | Gros volumes de données, tableaux de bord permanents |

Nous allons voir les 3, mais je recommande de commencer par l'**Export manuel** pour comprendre vos données, puis de passer à l'**OData** ou l'**API REST** pour l'automatisation.

---

## 2. Prérequis avant de commencer

1. **Un compte KoboToolbox Humanitarian actif** sur `kobo.humanitarianresponse.info`
2. **Power BI Desktop installé** (gratuit, à télécharger depuis le Microsoft Store ou powerbi.microsoft.com)
3. **Un formulaire déjà créé et avec des données collectées** (au moins quelques réponses pour tester)
4. Votre **jeton API (API Token)** ou vos identifiants de connexion Kobo

### 2.1 Récupérer votre jeton API (API Token)

C'est l'étape la plus importante, faites-la en premier :

1. Connectez-vous sur https://kobo.humanitarianresponse.info
2. Cliquez sur votre profil (en haut à droite) → **Account Settings**
3. Dans le menu de gauche, cherchez **"Security"** ou allez directement à l'URL :
   `https://kobo.humanitarianresponse.info/token/?format=json`
4. Vous verrez une longue chaîne de caractères comme `token=abcd1234efgh5678...` → **copiez-la et gardez-la précieusement** (ne la partagez jamais, c'est comme un mot de passe)

---

## 3. Méthode 1 — Export manuel (pour débuter en douceur)

C'est la méthode la plus simple pour un premier test.

### Étapes :

1. Connectez-vous à KoboToolbox Humanitarian
2. Ouvrez votre projet/formulaire
3. Allez dans l'onglet **"Data" (Données)** → **"Downloads"**
4. Choisissez le format :
   - **XLSX** (recommandé, le plus simple pour Power BI)
   - **CSV**
5. Sélectionnez les options :
   - Type d'export : **"Include groups in headers"** décoché si vous n'avez pas de groupes imbriqués complexes
   - Cochez **"Include all versions"** si votre formulaire a été modifié plusieurs fois
6. Cliquez sur **Export**, puis téléchargez le fichier une fois généré

### Dans Power BI Desktop :

1. Ouvrez Power BI Desktop
2. **Accueil → Obtenir les données → Classeur Excel** (ou "Texte/CSV")
3. Sélectionnez votre fichier téléchargé
4. Choisissez la feuille contenant vos données (souvent nommée comme votre formulaire)
5. Cliquez sur **Charger** (ou **Transformer les données** pour nettoyer avant de charger — recommandé, voir section 6)

⚠️ **Limite** : à chaque nouvelle collecte de données sur le terrain, il faudra refaire cet export manuellement et recharger le fichier. Pour éviter cela, passez à la méthode 2 ou 3.

---

## 4. Méthode 2 — Connexion via l'API REST de KoboToolbox (recommandé)

Cette méthode permet à Power BI d'aller chercher directement les données à jour sur le serveur Kobo, sans passer par un export manuel.

### 4.1 Trouver l'URL de l'API de votre formulaire

1. Dans KoboToolbox, ouvrez votre formulaire
2. Allez dans l'onglet **"Data" → "Downloads"** (ou "API" selon la version de l'interface)
3. Repérez l'**ID de l'asset** (asset uid), une chaîne du type `aXXXXXXXXXXXXXXXXXXXXXX`, visible dans l'URL de votre formulaire (ex : `.../#/forms/aXbYcZ.../summary`)
4. L'URL de l'API pour récupérer les données en JSON est généralement :

```
https://kobo.humanitarianresponse.info/api/v2/assets/{asset_uid}/data/?format=json
```

Remplacez `{asset_uid}` par l'identifiant de votre formulaire.

### 4.2 Se connecter depuis Power BI

1. Ouvrez Power BI Desktop
2. **Accueil → Obtenir les données → Web**
3. Choisissez **"Avancé"** (Advanced) pour pouvoir ajouter l'en-tête d'authentification
4. Dans **"URL de base"**, collez l'URL de l'API (ci-dessus)
5. Dans la section **"En-têtes de requête HTTP"** (Request Headers), ajoutez :
   - Nom de l'en-tête : `Authorization`
   - Valeur : `Token VOTRE_TOKEN_ICI` (attention : le mot **"Token"** suivi d'un espace, puis votre jeton copié à l'étape 2.1)
6. Cliquez sur **OK**
7. Power BI va se connecter et afficher les données au format JSON — cliquez sur **"Vers la table"** (To Table) puis développez les colonnes avec les petites flèches ⬇️ pour transformer le JSON en tableau lisible
8. Cliquez sur **Charger** ou **Transformer les données**

### 4.3 Activer l'actualisation automatique

Une fois publié sur le **service Power BI** (powerbi.com) :

1. Publiez votre rapport (**Accueil → Publier**)
2. Sur powerbi.com, allez dans les paramètres du dataset (jeu de données)
3. Dans **"Informations d'identification de la source de données"**, entrez à nouveau votre clé/authentification
4. Configurez une **actualisation planifiée** (Scheduled refresh) — par exemple tous les jours ou plusieurs fois par jour

---

## 5. Méthode 3 — Connecteur OData (pour tableaux de bord permanents)

KoboToolbox propose une URL **OData**, un format standardisé que Power BI sait lire nativement de façon très fluide (sans manipulation de JSON).

### 5.1 Trouver le lien OData

1. Dans votre formulaire KoboToolbox → **Data → Downloads** (ou **"Sync"** selon la version)
2. Cherchez le lien **"OData"** ou construisez-le ainsi :

```
https://kobo.humanitarianresponse.info/api/v2/assets/{asset_uid}/data.svc/
```

### 5.2 Se connecter depuis Power BI

1. **Accueil → Obtenir les données → OData Feed**
2. Collez l'URL OData ci-dessus
3. Quand Power BI demande l'authentification, choisissez **"Base"** (Basic) et entrez :
   - Nom d'utilisateur : votre identifiant Kobo
   - Mot de passe : votre mot de passe Kobo (ou le token selon la configuration)
4. Cliquez sur **Se connecter**, puis sélectionnez la table de données à charger
5. **Charger**

✅ Avantage : cette méthode gère automatiquement les tableaux liés (répétitions, groupes) et est plus stable pour de gros volumes de données.

---

## 6. Nettoyer et préparer vos données (Power Query)

Une fois les données chargées, avant de créer vos visualisations, nettoyez-les dans l'**Éditeur Power Query** (bouton **Transformer les données**) :

1. **Supprimer les colonnes inutiles** : clic droit sur une colonne → *Supprimer*
   - Souvent à supprimer : `_uuid`, `formhub/uuid`, `meta/instanceID`, colonnes techniques
2. **Renommer les colonnes** en langage clair (double-clic sur l'en-tête)
3. **Corriger les types de données** : sélectionnez une colonne → onglet *Accueil* → *Type de données* (Date, Nombre, Texte...)
4. **Gérer les valeurs manquantes** : *Transformer → Remplacer les valeurs*
5. Pour les **questions à choix multiples** (souvent stockées en une seule colonne séparée par des espaces), utilisez *Fractionner la colonne → Par délimiteur*
6. Pour les **géolocalisations** (format `latitude longitude altitude précision`), fractionnez également par espace pour créer des colonnes Latitude/Longitude utilisables dans une carte Power BI

Cliquez sur **Fermer et appliquer** une fois terminé.

---

## 7. Bonnes pratiques pour débutants

- ✅ **Commencez petit** : testez d'abord avec l'export manuel (méthode 1) pour bien comprendre la structure de vos données avant d'automatiser
- ✅ **Ne partagez jamais votre token API** — c'est équivalent à un mot de passe
- ✅ **Documentez vos transformations** dans Power Query (les étapes sont listées à droite, vous pouvez les renommer)
- ✅ **Créez une colonne "Date d'actualisation"** avec `DateTime.LocalNow()` en requête personnalisée pour savoir quand les données ont été mises à jour pour la dernière fois
- ✅ **Séparez les données brutes et les visuels** : gardez une page "Data check" dans votre rapport Power BI pour vérifier rapidement le nombre de lignes/dernière date de collecte
- ⚠️ Si votre formulaire a des **répétitions/groupes** (repeat groups), les données seront réparties dans plusieurs tables — c'est normal, il faudra créer des relations entre elles dans Power BI (onglet **Modèle**)

---

## 8. Dépannage — erreurs courantes

| Erreur | Cause probable | Solution |
|---|---|---|
| `401 Unauthorized` ou `403 Forbidden` | Token incorrect ou mal formaté | Vérifiez que vous avez bien écrit `Token ` (avec un espace) avant votre clé |
| Données vides ou incomplètes | Mauvais `asset_uid` dans l'URL | Revérifiez l'ID du formulaire dans l'URL de Kobo |
| Erreur de connexion réseau dans Power BI Service | Source de données non configurée pour l'actualisation | Ajoutez les identifiants dans les paramètres du dataset sur powerbi.com |
| JSON illisible / colonnes en `Record` ou `List` | Structure imbriquée (groupes/répétitions) | Cliquez sur les flèches ⬇️ à côté du nom de colonne pour "développer" |
| Données dupliquées après actualisation | Erreur commune côté KoboToolbox si les paramètres de pagination changent | Vérifiez que l'URL n'a pas de paramètre `limit` trop restrictif ; augmentez-le si besoin (ex : `&limit=30000`) |

---

## 9. Ressources utiles

- Documentation officielle KoboToolbox API : https://support.kobotoolbox.org/api.html
- Documentation Power Query / Power BI : https://learn.microsoft.com/power-query/
- Serveur Humanitarian : https://kobo.humanitarianresponse.info

---

## Résumé rapide (pour aller vite)

1. Récupérez votre **token API** sur Kobo Humanitarian
2. Testez d'abord avec un **export XLSX manuel** pour comprendre vos données
3. Passez à l'**API REST** (`Obtenir les données → Web → Avancé` + en-tête `Authorization: Token ...`) ou à l'**OData** pour l'automatisation
4. Nettoyez vos données dans **Power Query**
5. Publiez sur **powerbi.com** et configurez l'**actualisation planifiée**
