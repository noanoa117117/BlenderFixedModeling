using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
public static class ApplyLasyushaV002
{
    const string Work = "E:/BlenderHairWorkflow/artifacts/";
    const string Folder = "Assets/HairFit_Lasyusha/v002";
    static ApplyLasyushaV002() { EditorApplication.update += Poll; }
    static void Poll()
    {
        string file=Work+"unity-command.txt";
        if(EditorApplication.isCompiling || EditorApplication.isUpdating || !File.Exists(file)) return;
        string command=File.ReadAllText(file).Trim(); File.Delete(file);
        try
        {
            if(command=="audit") Audit();
            else if(command=="apply") Apply();
            else if(command=="integrate") Integrate();
            else if(command.StartsWith("view ")) View(float.Parse(command.Substring(5),System.Globalization.CultureInfo.InvariantCulture));
            else if(command=="save") { if(EditorApplication.isPlaying)throw new Exception("Do not save during Play Mode"); EditorSceneManager.SaveScene(SceneManager.GetActiveScene()); File.WriteAllText(Work+"unity-result.txt","saved"); }
        }
        catch(Exception e) { File.WriteAllText(Work+"unity-result.txt",e.ToString()); Debug.LogException(e); }
    }
    static GameObject Hair(string name="lasyusha")
    {
        var matches=SceneManager.GetActiveScene().GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).Where(t=>t.name==name).ToArray();
        if(matches.Length!=1) throw new Exception("Expected one "+name+", found "+matches.Length);
        return matches[0].gameObject;
    }
    [MenuItem("Tools/HairFit/Audit scene hair")]
    public static void Audit()
    {
        var h=Hair();
        var data=new JObject { ["scene"]=SceneManager.GetActiveScene().path,["dirty"]=SceneManager.GetActiveScene().isDirty,["rootPosition"]=h.transform.position.ToString("F5"),["rootScale"]=h.transform.lossyScale.ToString("F5"),["prefab"]=PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(h),["components"]=new JArray(h.GetComponentsInChildren<Component>(true).Where(c=>c!=null).Select(c=>c.GetType().FullName).Distinct()) };
        data["renderers"]=new JArray(h.GetComponentsInChildren<Renderer>(true).Select(r=>new JObject { ["name"]=r.name,["position"]=r.transform.position.ToString("F5"),["bounds"]=r.bounds.ToString(),["materials"]=new JArray(r.sharedMaterials.Select(m=>m?AssetDatabase.GetAssetPath(m):"null")),["bones"]=new JArray(r is SkinnedMeshRenderer s?s.bones.Select(b=>b?b.name:"null"):new string[0]) }));
        data["transforms"]=new JArray(h.GetComponentsInChildren<Transform>(true).Select(t=>new JObject{["name"]=t.name,["parent"]=t.parent?t.parent.name:"",["position"]=t.position.ToString("F5")}));
        data["settings"]=new JArray(h.GetComponentsInChildren<MonoBehaviour>(true).Where(c=>c!=null && c.GetType().Name.StartsWith("Modular")).Select(c=>EditorJsonUtility.ToJson(c)));
        File.WriteAllText(Work+"unity-audit.json",data.ToString()); File.WriteAllText(Work+"unity-result.txt","audit complete");
    }
    static Vector3 V(JToken t) {return new Vector3((float)t[0],(float)t[1],(float)t[2]);}
    static void Integrate()
    {
        var h=Hair("lasyusha_Blender_v002");
        var avatar=SceneManager.GetActiveScene().GetRootGameObjects().Single(g=>g.name=="Sepha (SPS) (ChichiwoMore)");
        Undo.SetTransformParent(h.transform,avatar.transform,"Attach Lasyusha to avatar");
        foreach(var r in h.GetComponentsInChildren<SkinnedMeshRenderer>(true))
        {
            var mesh=r.sharedMesh;mesh.name=Path.GetFileNameWithoutExtension(AssetDatabase.GetAssetPath(mesh));EditorUtility.SetDirty(mesh);
        }
        PrefabUtility.SaveAsPrefabAssetAndConnect(h,Folder+"/lasyusha_Blender_v002.prefab",InteractionMode.AutomatedAction);
        EditorSceneManager.MarkSceneDirty(h.scene);AssetDatabase.SaveAssets();
        File.WriteAllText(Work+"unity-result.txt","integrated under "+avatar.name);
    }
    [MenuItem("Tools/HairFit/Import evaluated Lasyusha v002")]
    public static void Apply()
    {
        if(EditorApplication.isPlaying) throw new Exception("Exit play mode before applying");
        var original=Hair();
        if(SceneManager.GetActiveScene().GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).Any(g=>g.name=="lasyusha_Blender_v002")) throw new Exception("New hair already exists; inspect before repeating");
        var data=JArray.Parse(File.ReadAllText(Work+"unity-evaluated.json"));
        EditorSceneManager.SaveScene(SceneManager.GetActiveScene(),"HairFit-Lasyusha-20260916/BeforeUnityV002.unity",true);
        var clone=UnityEngine.Object.Instantiate(original,original.transform.parent);
        clone.name="lasyusha_Blender_v002";
        if(PrefabUtility.IsPartOfPrefabInstance(clone)) PrefabUtility.UnpackPrefabInstance(clone,PrefabUnpackMode.Completely,InteractionMode.AutomatedAction);
        try
        {
            var transforms=clone.GetComponentsInChildren<Transform>(true);
            var boneMap=transforms.GroupBy(t=>t.name).ToDictionary(g=>g.Key,g=>g.First());
            var reports=new JArray();
            foreach(JObject item in data)
            {
                string name=(string)item["name"];
                var target=transforms.FirstOrDefault(t=>t.name==name);
                if(target==null) {target=new GameObject(name).transform; target.SetParent(clone.transform,false);}
                var old=target.GetComponent<Renderer>();
                var materials=old?old.sharedMaterials:transforms.First(t=>t.name=="back").GetComponent<Renderer>().sharedMaterials;
                target.localPosition=Vector3.zero;target.localRotation=Quaternion.identity;target.localScale=Vector3.one;
                var vertices=(JArray)item["vertices"];
                var names=vertices.SelectMany(v=>v["bones"].Values<string>()).Concat(new[]{"アーマチュア"}).Distinct().ToArray();
                foreach(string bone in names) if(!boneMap.ContainsKey(bone)) throw new Exception(name+": missing bone "+bone);
                var bones=names.Select(n=>boneMap[n]).ToArray();
                var indices=names.Select((n,i)=>new {n,i}).ToDictionary(x=>x.n,x=>x.i);
                var mesh=new Mesh {name=name.Replace(" ","_")+"_evaluated",indexFormat=UnityEngine.Rendering.IndexFormat.UInt32};
                var p=new Vector3[vertices.Count]; var nrm=new Vector3[p.Length];var uv=new Vector2[p.Length];var weights=new BoneWeight[p.Length];
                var inv=target.worldToLocalMatrix;
                for(int i=0;i<p.Length;i++)
                {
                    var v=vertices[i];p[i]=inv.MultiplyPoint3x4(V(v["p"]));nrm[i]=target.localToWorldMatrix.transpose.MultiplyVector(V(v["n"])).normalized;uv[i]=new Vector2((float)v["uv"][0],(float)v["uv"][1]);
                    var wn=v["bones"].Values<string>().ToArray(); var ww=v["weights"].Values<float>().ToArray(); float sum=ww.Sum();
                    if(sum<=0){wn=new[]{"アーマチュア"};ww=new[]{1f};sum=1;}
                    var bi=new int[4];var bw=new float[4];for(int j=0;j<wn.Length;j++){bi[j]=indices[wn[j]];bw[j]=ww[j]/sum;}
                    weights[i]=new BoneWeight {boneIndex0=bi[0],boneIndex1=bi[1],boneIndex2=bi[2],boneIndex3=bi[3],weight0=bw[0],weight1=bw[1],weight2=bw[2],weight3=bw[3]};
                }
                mesh.vertices=p;mesh.normals=nrm;mesh.uv=uv;mesh.subMeshCount=item["triangles"].Count();
                for(int i=0;i<mesh.subMeshCount;i++)mesh.SetTriangles(item["triangles"][i].Values<int>().ToArray(),i);
                if(bones.Length>0){mesh.boneWeights=weights;mesh.bindposes=bones.Select(b=>b.worldToLocalMatrix*target.localToWorldMatrix).ToArray();}
                mesh.RecalculateBounds();mesh.RecalculateTangents();
                string path=Folder+"/"+name.Replace(" ","_")+"_evaluated.asset";
                var existing=AssetDatabase.LoadAssetAtPath<Mesh>(path);
                if(existing){EditorUtility.CopySerialized(mesh,existing);UnityEngine.Object.DestroyImmediate(mesh);mesh=existing;}else AssetDatabase.CreateAsset(mesh,path);
                if(bones.Length>0)
                {
                    if(old && !(old is SkinnedMeshRenderer))UnityEngine.Object.DestroyImmediate(old);
                    var filter=target.GetComponent<MeshFilter>();if(filter)UnityEngine.Object.DestroyImmediate(filter);
                    var r=target.GetComponent<SkinnedMeshRenderer>();if(!r)r=target.gameObject.AddComponent<SkinnedMeshRenderer>();
                    r.sharedMesh=mesh;r.bones=bones;r.rootBone=boneMap["アーマチュア"];r.sharedMaterials=materials;r.localBounds=mesh.bounds;r.updateWhenOffscreen=true;
                    var baked=new Mesh();r.BakeMesh(baked);float max=0;var bv=baked.vertices;
                    for(int i=0;i<bv.Length;i++)max=Mathf.Max(max,Vector3.Distance(target.TransformPoint(bv[i]),V(vertices[i]["p"])));
                    UnityEngine.Object.DestroyImmediate(baked);
                    reports.Add(new JObject{["name"]=name,["vertices"]=p.Length,["bones"]=bones.Length,["maxWorldError"]=max});
                    if(max>0.0005f)throw new Exception(name+": skinning validation error "+max);
                }
                else
                {
                    if(old && !(old is MeshRenderer))UnityEngine.Object.DestroyImmediate(old);
                    (target.GetComponent<MeshFilter>()??target.gameObject.AddComponent<MeshFilter>()).sharedMesh=mesh;
                    (target.GetComponent<MeshRenderer>()??target.gameObject.AddComponent<MeshRenderer>()).sharedMaterials=materials;
                    reports.Add(new JObject{["name"]=name,["vertices"]=p.Length,["bones"]=0});
                }
                target.gameObject.SetActive((bool)item["enabled"]);
            }
            foreach(var modifier in clone.GetComponentsInChildren<MonoBehaviour>(true).Where(c=>c!=null && c.GetType().Name=="ModularAvatarShapeChanger").ToArray()) UnityEngine.Object.DestroyImmediate(modifier);
            PrefabUtility.SaveAsPrefabAssetAndConnect(clone,Folder+"/lasyusha_Blender_v002.prefab",InteractionMode.AutomatedAction);
            Undo.RegisterCreatedObjectUndo(clone,"Import fitted Lasyusha");Undo.RecordObject(original,"Replace fitted Lasyusha");original.SetActive(false);
            EditorSceneManager.MarkSceneDirty(clone.scene);AssetDatabase.SaveAssets();Selection.activeGameObject=clone;
            File.WriteAllText(Work+"unity-validation.json",reports.ToString());File.WriteAllText(Work+"unity-result.txt","applied: "+clone.name);
        }
        catch {UnityEngine.Object.DestroyImmediate(clone);throw;}
    }
    static void View(float yaw)
    {
        var scene=SceneView.lastActiveSceneView;
        var pivot=new Vector3(0,1.3f,0);var h=Hair("lasyusha_Blender_v002");var r=h.GetComponentsInChildren<Renderer>().First(x=>x.name=="back");pivot.x=r.bounds.center.x;pivot.z=r.bounds.center.z;
        scene.orthographic=false;scene.LookAtDirect(pivot,Quaternion.Euler(5,yaw,0),0.30f);scene.Repaint();Selection.activeObject=null;
        File.WriteAllText(Work+"unity-result.txt","view "+yaw);
    }
}
