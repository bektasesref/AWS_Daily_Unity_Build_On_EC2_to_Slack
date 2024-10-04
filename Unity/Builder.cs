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
#if UNITY_EDITOR
        public static void BuildForAndroid()
        {
            PlayerSettings.Android.useCustomKeystore = false;
            DoBuild(Path.Combine(Application.dataPath.Replace("/Assets", ""), "BuildForAndroid", "Build.apk"), BuildTarget.Android);
        }
        public static void BuildForiOS()
        {
            DoBuild(Path.Combine(Application.dataPath.Replace("/Assets", ""), "BuildForiOS"), BuildTarget.iOS);
        }
        public static void DoBuild(string locationPathName, BuildTarget target)
        {
            BuildPlayerOptions buildPlayerOptions = new BuildPlayerOptions();
            for (int i = 0; i < EditorBuildSettings.scenes.Length; i++)
                scenes.Add(AssetDatabase.GUIDToAssetPath(EditorBuildSettings.scenes[i].guid));
            buildPlayerOptions.scenes = scenes.ToArray();
            buildPlayerOptions.locationPathName = locationPathName;
            buildPlayerOptions.target = target;
            buildPlayerOptions.options = BuildOptions.CompressWithLz4HC;
            BuildPipeline.BuildPlayer(buildPlayerOptions);
        }
#endif
    }
}