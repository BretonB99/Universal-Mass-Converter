# Guide d'installation de FFmpeg

**FFmpeg** est un outil gratuit et open-source indispensable pour activer les fonctionnalités **Audio**, **Vidéo**, **GIF** et **l'extraction de sous-titres** dans *Universal Mass Converter*.

Si FFmpeg n'est pas installé, l'indicateur en haut de l'application affichera **`● FFmpeg absent`**, mais toutes les autres conversions (Images, PDF, Documents, Données, etc.) continueront de fonctionner normalement.

---

## 1. Installation sous Windows (Recommandé)

### Méthode rapide via PowerShell (en 1 commande)
1. Ouvrez le menu **Démarrer**, tapez **`PowerShell`** et ouvrez-le.
2. Copiez et collez la commande suivante, puis appuyez sur **Entrée** :
   ```powershell
   winget install Gyan.FFmpeg
   ```
3. Une fois l'installation terminée, **fermez et relancez** *Universal Mass Converter* (ou votre terminal). L'indicateur passera automatiquement au vert : **`● FFmpeg prêt`**.

### Méthode manuelle (si `winget` n'est pas disponible)
1. Rendez-vous sur le site officiel : [ffmpeg.org/download.html](https://ffmpeg.org) et téléchargez la version Windows (`gyan.dev` ou `BtbN`).
2. Extrayez l'archive ZIP dans un dossier fixe, par exemple `C:\ffmpeg`.
3. Ajoutez le sous-dossier `C:\ffmpeg\bin` aux **Variables d'environnement (Path)** de Windows :
   * Recherchez *« Modifier les variables d'environnement système »* dans le menu Démarrer.
   * Cliquez sur **Variables d'environnement...** > sélectionnez **Path** > **Modifier** > **Nouveau** > collez `C:\ffmpeg\bin`.
4. Validez avec **OK** et redémarrez l'application.

---

## 2. Installation sous macOS

Avec le gestionnaire de paquets **Homebrew**, ouvrez le Terminal et tapez :
```bash
brew install ffmpeg
```

---

## 3. Installation sous Linux

* **Ubuntu / Debian :**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
* **Fedora :**
  ```bash
  sudo dnf install ffmpeg
  ```
* **Arch Linux :**
  ```bash
  sudo pacman -S ffmpeg
  ```

---

## Vérifier que l'installation fonctionne
Ouvrez un terminal (PowerShell sous Windows) et tapez :
```bash
ffmpeg -version
```
Si des informations de version s'affichent, FFmpeg est prêt à être utilisé par le logiciel.
