using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build;
using UnityEngine;
using System.Collections.Generic;
using UnityEditor.Build.Reporting;

namespace YourGameNameSpace
{
#pragma warning disable CS0618
    [InitializeOnLoad]
    class Builder : IPostprocessBuildWithReport, IPreprocessBuildWithReport
#pragma warning restore CS0618
    {
        static Builder()
        {
            PlayerSettings.Android.useCustomKeystore = false;
            PlayerSettings.Android.keystorePass = "[corrupted]";
            PlayerSettings.Android.keyaliasName = "[corrupted]";
            PlayerSettings.Android.keyaliasPass = "[corrupted]";
        }
#if UNITY_EDITOR // necessary for not storing those values in a build for security reasons. Therefore binary won't hold the values
        public static void BuildForAndroid() // Used in Android build from terminal
        {
            PlayerSettings.Android.useCustomKeystore = false;

            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            List<string> scenes = new();
            for (int i = 1; i < EditorBuildSettings.scenes.Length; i++)
                scenes.Add(AssetDatabase.GUIDToAssetPath(EditorBuildSettings.scenes[i].guid));
            buildPlayerOptions.scenes = scenes.ToArray();
            buildPlayerOptions.locationPathName = Path.Combine(Application.dataPath.Replace("/Assets", ""), "BuildForAndroid", "Build.apk");
            buildPlayerOptions.target = BuildTarget.Android;
            buildPlayerOptions.options = BuildOptions.CompressWithLz4HC;
            BuildPipeline.BuildPlayer(buildPlayerOptions);
        }
#endif
    }
}