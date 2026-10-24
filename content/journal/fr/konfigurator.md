# Le configurateur 3D génératif Vargov®Design

Rubrique: Fabrication · Date: 31 août 2026 · Slug: konfigurator

Le configurateur 3D génératif assemble une composition suspendue à partir des éléments de la marque, la montre en volume et livre la spécification qui servira à la fabriquer.

D'ordinaire, le choix d'une lumière d'auteur se passe ainsi : l'architecte trouve une composition dans le catalogue, écrit un courriel, décrit avec des mots la taille et la densité voulues — puis attend. Un jour plus tard arrive une image de synthèse. Quelque chose cloche : trop d'éléments, la silhouette n'y est pas. Encore un courriel, encore un jour.

Le configurateur supprime cet échange. La composition s'assemble directement dans le navigateur, en quelques minutes, et se voit aussitôt en volume.

Ce qu'il fait

Vous indiquez une référence du catalogue et les dimensions du nuage en millimètres — le moteur récupère les tailles réelles de l'élément, sa puissance et sa forme tridimensionnelle. Vient ensuite la forme de la composition elle-même : cube, sphère, demi-sphère, cône, cylindre, pyramide, cascade, anneau, vague, spirale, goutte, lentille, entonnoir, cadre, arc, serpentin, hélice, étages, coupe, coin ou bioforme — vingt et une possibilités.

Densité aérée, moyenne, dense — ou nombre exact d'éléments. Disposition verticale, horizontale, mixte ; rotation aléatoire, depuis le centre ou en trame régulière ; inclinaison sur tout axe de −90° à +90°. Deux références peuvent se mêler dans une même composition, dans la proportion choisie.

La couleur des éléments vient du nuancier RAL — 210 teintes avec recherche par code et par nom ; une même composition peut mêler jusqu'à huit couleurs du nuancier, chacune avec sa propre transparence (les rubans n'ont qu'une seule couleur de verre). S'y ajoutent les couleurs maison, la galvanoplastie (teintes transparentes et finitions miroir) et « Transparent incolore » ; la transparence n'est proposée que là où l'élément peut réellement être transparent. Pour les compositions dotées d'une quincaillerie métallique, le métal est défini par un code du catalogue des finitions JN — 24 échantillons, huit couleurs déclinées en trois finitions. Il n'y a volontairement pas de pipette dans le configurateur : la spécification porte un code RAL, le nom d'une finition galvanique ou un code JN — ce que la production saura réellement reproduire.

Une répartition qui ne ment pas

L'essentiel d'un assemblage génératif n'est pas la belle image mais l'honnêteté physique. Ni les éléments ni les câbles ne se croisent. Le câble de chaque élément est vérifié par rapport à son vrai point de fixation — douille sur certaines formes, perçage dans le verre sur d'autres — et par rapport à la silhouette réelle de ses voisins, relevée sur le modèle lui-même. La règle est contrôlée automatiquement avant chaque mise en production.

Une configuration donne toujours la même répartition : un confrère qui ouvre votre lien voit exactement la même chose. Le bouton de régénération propose une autre variante à densité égale.

Les rubans ont leur propre moteur : dix références se construisent non en nuage d'éléments mais en ruban continu de tubes de verre sur une armature — sa plastique, son métrage et son dégradé sur la longueur.

Les chiffres dont l'installateur a besoin

Le configurateur affiche le nombre d'éléments, les dimensions réelles du nuage, le point bas sous le plafond, la répartition par tailles, la puissance totale — et le poids de la composition, calculé automatiquement d'après ses éléments.

Le poids n'est pas une donnée d'appoint. Il détermine quelle cheville tient la suspension et s'il faut renforcer la dalle. Ce chiffre se calculait autrefois par courriel, une fois la liste des éléments arrêtée ; il est désormais là dès le début, à côté de la silhouette.

Ce que vous emportez

IFC4 pour le BIM : longueurs en millimètres, chaque point de fixation est un objet distinct portant le nombre d'éléments qui y sont suspendus et, lorsque la masse est connue, la charge calculée. Le modèle est construit sous un plafond à la hauteur saisie dans le champ « Hauteur sous plafond, mm », à côté du bouton IFC (2700 mm par défaut) : points de fixation au plafond, origine des coordonnées au sol. Une spécification PDF avec nomenclature, masse, puissance, montage, délai de fabrication et garantie, et un QR code vers la configuration elle-même. Une feuille d'appel d'offres pour les achats et la douane. Le plan DXF pour AutoCAD est réservé à un usage interne : la production et les revendeurs de la marque. Les modèles 3D prêts à l'emploi de la référence (max, fbx) se trouvent sur 3ddd.ru et 3dsky.org. La composition assemblée, elle, se télécharge en FBX pour 3ds Max, par le bouton placé à côté de l'export IFC : géométrie et couleurs en objets distincts, avec les fils et les fixations, en millimètres. Ce fichier ne porte aucune propriété BIM — celles-ci restent dans l'IFC4 ; les rubans n'ont pas cet export. Les projets enregistrés restent dans le navigateur lui-même, sans compte, et le lien porte l'état complet de la configuration.

La composition peut s'essayer dans votre pièce depuis un téléphone : USDZ sur iOS, GLB sur Android. L'interface fonctionne en huit langues, arabe de droite à gauche compris.

En quoi il diffère d'un configurateur ordinaire

La scène présente de vrais produits. Les formes sont relevées sur les modèles de production — épaisseur réelle des pièces, douilles et points où le câble se fixe en fabrication. Ni icônes ni sphères de substitution.

La composition est générée, non choisie dans une liste. Le moteur répartit les éléments dans le volume de la forme retenue en surveillant la silhouette et les jeux ; à partir du numéro de variante, la composition se reproduit bit à bit.

Les règles de la maison sont intégrées et vérifiées automatiquement. Le câble ne traverse jamais le verre — test de rayon sur les triangles du maillage ; les corps ne se touchent pas ; la pente du cône file droit du rang supérieur à la pointe. Ces gardiens tournent avant chaque mise en production.

La masse se déduit de la géométrie : coques selon l'épaisseur de paroi, tôle selon sa propre géométrie, pièces coulées au volume — et recoupée avec les expéditions d'usine.

Combien au total

Le configurateur compte des centaines de compositions lumineuses et décoratives. Celles qui s'ouvrent avec un calcul complet exportent aussitôt un modèle IFC4, une spécification PDF et une feuille d'appel d'offres. La densité de répartition est calibrée sur des commandes réelles. Chaque référence du configurateur a sa propre page en russe et en anglais ; les chiffres exacts à jour figurent sur la page du configurateur du site, où ils sont calculés à partir de ses données.

Un regard extérieur

Le configurateur 3D a été accepté et jugé sur Awwwards — la plateforme internationale qui sélectionne les meilleurs sites du monde sur le design, l'ergonomie, le contenu et la créativité. Statut : Nominee 2026. Pour un outil qui fait un travail pointu pour un public restreint, cela confirme qu'il reste commode même pour qui le découvre.

Où l'ouvrir

Hors de Russie — vargov.design. En Russie — configurator.vargov.ru.

La composition finie s'envoie à l'ingénieur-concepteur de la marque directement depuis le configurateur. Cliquez sur « Demander un devis » et choisissez Telegram, WhatsApp ou l'e-mail : le texte de la demande s'insère tout seul — il ne reste qu'à appuyer sur « Envoyer ». La réponse arrivera par le même canal.

Vargov®Design — pour ceux qui voient la différence.

Made in Vargov.
