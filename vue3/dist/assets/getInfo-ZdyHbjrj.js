import{_ as y,u as h,a as k,i as v,f as u,h as C,j as x,d as e,w as n,b as i,o as B,e as c,t as m,E as p,g as T}from"./index-NUoop2OX.js";const E={class:"user-list-container"},N={class:"user-list"},S={__name:"getInfo",setup(I){const _=h(),r=k([]);v(async()=>{try{const a=await u.post("/api/legymCustomer/get_info",{manager:_.manager});r.value=a.data.customers}catch(a){console.error("获取用户列表失败：",a)}});const g=async a=>{try{const s=await u.post("/api/legymCustomer/begin_state",{id:a.id,manager:_.manager,username:a.username});s.status===200&&(a.begin_state=s.data.begin_state,p.success(s.data.message))}catch(s){console.error("更新开始状态失败：",s),p.error("更新开始状态失败")}},b=async a=>{try{if(await T.confirm("确定要删除该用户吗？剩余乐点将返还。","警告",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"})==="confirm"){const t=await u.post("/api/legymCustomer/delete",{id:a.id,manager:_.manager,username:a.username});t.status===200&&(r.value=r.value.filter(l=>l.username!==a.username),p.success(t.data.message))}}catch(s){s!=="cancel"&&(console.error("删除用户失败：",s),p.error("删除用户失败"))}};return(a,s)=>{const t=i("el-table-column"),l=i("el-tag"),d=i("el-button"),f=i("el-table");return B(),C("div",E,[x("div",N,[e(f,{data:r.value,stripe:""},{default:n(()=>[e(t,{prop:"manager",label:"管理员"}),e(t,{prop:"create_time",label:"创建时间",width:"170"}),e(t,{prop:"username",label:"用户名",width:"120"}),e(t,{prop:"password",label:"密码",width:"120"}),e(t,{prop:"schoolName",label:"学校"}),e(t,{prop:"runType",label:"跑步类型"}),e(t,{prop:"runTime",label:"跑步时间"}),e(t,{prop:"day_goals",label:"每日目标(km)"}),e(t,{prop:"day_in_week",label:"每周目标(天)"}),e(t,{prop:"complete_day_in_week",label:"已完成(天)"}),e(t,{prop:"total_goals",label:"总目标(km)"}),e(t,{prop:"complete_goals",label:"已完成(km)"}),e(t,{label:"跑步状态",width:"100"},{default:n(o=>[e(l,{type:o.row.is_run?"success":"info"},{default:n(()=>[c(m(o.row.is_run?"已完成":"未完成"),1)]),_:2},1032,["type"])]),_:1}),e(t,{label:"开始状态",width:"100"},{default:n(o=>[e(l,{type:o.row.begin_state?"success":"info"},{default:n(()=>[c(m(o.row.begin_state?"进行中":"暂停中"),1)]),_:2},1032,["type"])]),_:1}),e(t,{label:"操作",width:"150"},{default:n(o=>[e(d,{size:"small",type:o.row.begin_state?"warning":"success",onClick:w=>g(o.row)},{default:n(()=>[c(m(o.row.begin_state?"暂停":"开始"),1)]),_:2},1032,["type","onClick"]),e(d,{size:"small",type:"danger",onClick:w=>b(o.row)},{default:n(()=>s[0]||(s[0]=[c(" 删除 ")])),_:2},1032,["onClick"])]),_:1})]),_:1},8,["data"])])])}}},V=y(S,[["__scopeId","data-v-f740281f"]]);export{V as default};
