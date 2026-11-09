(function(){
  var $=function(s,c){return (c||document).querySelector(s)};
  var $$=function(s,c){return [].slice.call((c||document).querySelectorAll(s))};

  // Header
  var hdr=$('#hdr');
  if(hdr && !hdr.classList.contains('fixed-solid')){
    var onScroll=function(){hdr.classList.toggle('solid',window.scrollY>40)};
    window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  }
  var menu=$('#menu'),burger=$('#burger');
  if(menu&&burger){
    burger.onclick=function(){menu.classList.toggle('open')};
    $$('a',menu).forEach(function(a){a.addEventListener('click',function(){menu.classList.remove('open')})});
  }

  // Reveal
  var io='IntersectionObserver' in window?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1}):null;
  $$('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});

  // Gallery filter (trang chủ)
  var items=$$('.gi');
  var filters=$('#filters');
  if(filters){
    filters.addEventListener('click',function(e){
      var b=e.target.closest('button');if(!b)return;
      $$('button',filters).forEach(function(x){x.classList.toggle('on',x===b)});
      var f=b.dataset.f;items.forEach(function(it){it.classList.toggle('hide',f!=='all'&&it.dataset.g!==f)});
    });
  }

  // Lightbox (dùng chung)
  var lb=$('#lb');
  if(lb&&items.length){
    var lbi=$('img',lb),lbc=$('.lbc',lb),cur=0;
    var vis=function(){return items.filter(function(i){return !i.classList.contains('hide')})};
    var show=function(i){var v=vis();cur=(i+v.length)%v.length;var it=v[cur];lbi.src=$('img',it).src;var b=$('b',it),l=$('.lbl',it);lbc.textContent=(b?b.textContent:'')+(l?' — '+l.textContent:'');lb.classList.add('on')};
    items.forEach(function(it){it.addEventListener('click',function(){show(vis().indexOf(it))})});
    $('.x',lb).onclick=function(){lb.classList.remove('on')};
    $('.pv',lb).onclick=function(e){e.stopPropagation();show(cur-1)};
    $('.nx',lb).onclick=function(e){e.stopPropagation();show(cur+1)};
    lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('on')});
    document.addEventListener('keydown',function(e){if(!lb.classList.contains('on'))return;if(e.key==='Escape')lb.classList.remove('on');if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
  }

  // Ước tính chi phí
  var est=$('#est');
  if(est){
    var area=$('#est-area'),out=$('#est-out'),note=$('#est-note');
    var fmt=function(n){return (Math.round(n/1e6*10)/10).toLocaleString('vi-VN')};
    var calc=function(){
      var g=$('input[name=goi]:checked',est);var a=parseFloat((area.value||'').replace(',','.'));
      $$('.goi',est).forEach(function(l){l.classList.toggle('on',$('input',l).checked)});
      if(!g||!a||a<=0){out.textContent='—';note.textContent='Nhập diện tích để xem khoảng chi phí.';return}
      var lo=+g.dataset.lo*1e6*a,hi=+g.dataset.hi*1e6*a;
      out.textContent=fmt(lo)+' – '+fmt(hi)+' triệu đồng';
      note.textContent='Tạm tính cho '+a+' m² × '+g.dataset.lo.replace('.',',')+'–'+g.dataset.hi.replace('.',',')+' triệu/m², chưa VAT. Báo giá chính xác cần khảo sát và bản vẽ.';
    };
    est.addEventListener('input',calc);est.addEventListener('change',calc);calc();
  }

  // Form báo giá (demo: chưa nối Formspree)
  var form=$('#qform');
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var g=function(id){var el=document.getElementById(id);return el?el.value.trim():''};
      var ok=true;['name','phone'].forEach(function(id){var el=document.getElementById(id);var bad=!el.value.trim();el.style.borderColor=bad?'#d64545':'';if(bad)ok=false});
      if(!ok)return;
      var s='YÊU CẦU BÁO GIÁ – NHẬT KHANG\nHọ tên: '+g('name')+'\nSĐT/Zalo: '+g('phone')+'\nLoại công trình: '+g('type')+'\nDiện tích: '+(g('area')||'—')+' m²\nDự án/toà: '+(g('proj')||'—')+'\nHạng mục: '+g('scope')+'\nGhi chú: '+(g('msg')||'—');
      $('#summary').textContent=s;$('#fbody').style.display='none';$('#done').style.display='block';
    });
    var cp=$('#copy');
    if(cp)cp.addEventListener('click',function(){
      var t=$('#summary').textContent;
      try{navigator.clipboard.writeText(t).then(function(){cp.textContent='Đã sao chép ✓'},function(){cp.textContent='Hãy bôi đen để sao chép'})}catch(err){cp.textContent='Hãy bôi đen để sao chép'}
    });
  }
  var yr=$('#yr');if(yr)yr.textContent=new Date().getFullYear();
})();
