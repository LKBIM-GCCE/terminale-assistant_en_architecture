/* Site de la classe TEB-AA : dates, saisies enregistrées sur le poste, tableau éditable, export CSV */
(function () {
  var store = {
    get: function (k) { try { return localStorage.getItem('tebaa:' + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('tebaa:' + k, v); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem('tebaa:' + k); } catch (e) {} },
    keys: function () { var out = []; try { for (var i = 0; i < localStorage.length; i++) out.push(localStorage.key(i)); } catch (e) {} return out; }
  };

  // Séances passées / prochaine
  var today = new Date(); today.setHours(0, 0, 0, 0);
  var groups = {};
  document.querySelectorAll('[data-date]').forEach(function (el) {
    var d = new Date(el.getAttribute('data-date') + 'T00:00:00');
    var g = el.parentElement; var id = g ? (g.className || 'x') : 'x';
    if (d < today) el.classList.add('is-past');
    else if (!groups[id] && el.tagName !== 'SECTION') { groups[id] = true; el.classList.add('is-next'); }
  });

  // Barre de progression des projets
  document.querySelectorAll('.progress[data-dates]').forEach(function (bar) {
    var ds = bar.getAttribute('data-dates').split(' ').filter(Boolean);
    var done = ds.filter(function (d) { return new Date(d + 'T23:59:59') < new Date(); }).length;
    bar.querySelector('.progress-bar').style.width = (100 * done / ds.length) + '%';
    bar.querySelector('.progress-label').textContent = done + ' / ' + ds.length + ' séances';
  });

  // Les zones de texte s'agrandissent avec leur contenu (écran et impression)
  function grow(el) { if (el.tagName !== 'TEXTAREA') return; el.style.height = 'auto'; el.style.height = (el.scrollHeight + 4) + 'px'; }
  window.addEventListener('beforeprint', function () { document.querySelectorAll('textarea').forEach(grow); });

  // Champs texte, zones de texte, cases et boutons radio
  document.querySelectorAll('input[data-store], textarea[data-store]').forEach(function (el) {
    var k = el.getAttribute('data-store'), v = store.get(k);
    if (el.type === 'checkbox') { el.checked = v === '1'; el.addEventListener('change', function () { store.set(k, el.checked ? '1' : '0'); }); }
    else if (el.type === 'radio') { el.checked = v === el.value; el.addEventListener('change', function () { if (el.checked) store.set(k, el.value); }); }
    else {
      if (v !== null) el.value = v;
      el.addEventListener('input', function () { store.set(k, el.value); grow(el); });
      grow(el);
    }
  });

  // Tableau éditable
  function cols(t) { return parseInt(t.getAttribute('data-cols'), 10); }
  function addRow(t, values) {
    var tr = document.createElement('tr');
    for (var i = 0; i < cols(t); i++) {
      var td = document.createElement('td'); td.contentEditable = 'true'; td.textContent = values ? (values[i] || '') : '';
      td.addEventListener('input', function () { save(t); }); tr.appendChild(td);
    }
    var tdx = document.createElement('td'); var b = document.createElement('button');
    b.type = 'button'; b.className = 'del-row'; b.textContent = '×'; b.setAttribute('aria-label', 'Supprimer la ligne');
    b.addEventListener('click', function () { tr.remove(); save(t); }); tdx.appendChild(b); tr.appendChild(tdx);
    t.tBodies[0].appendChild(tr); return tr;
  }
  function rows(t) {
    return Array.prototype.map.call(t.tBodies[0].querySelectorAll('tr:not(.exemple)'), function (tr) {
      return Array.prototype.slice.call(tr.children, 0, cols(t)).map(function (td) { return td.textContent.trim(); });
    });
  }
  function save(t) { store.set(t.getAttribute('data-store'), JSON.stringify(rows(t))); }
  document.querySelectorAll('table.editable').forEach(function (t) {
    var data = null; try { data = JSON.parse(store.get(t.getAttribute('data-store')) || 'null'); } catch (e) {}
    if (data && data.length) data.forEach(function (r) { addRow(t, r); }); else { var n = parseInt(t.getAttribute('data-rows') || '5', 10); for (var i = 0; i < n; i++) addRow(t); }
  });

  // Boutons
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-action]'); if (!b) return;
    var a = b.getAttribute('data-action');
    if (a === 'add-row') { var t = document.getElementById(b.getAttribute('data-target')); addRow(t).firstChild.focus(); save(t); }
    if (a === 'print') window.print();
    if (a === 'export-csv') {
      var t2 = document.getElementById(b.getAttribute('data-target'));
      var head = Array.prototype.slice.call(t2.tHead.rows[0].cells, 0, cols(t2)).map(function (th) { return th.textContent; });
      var lines = [head].concat(rows(t2)).map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(';'); });
      var blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
      var link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = b.getAttribute('data-file') || 'export.csv';
      document.body.appendChild(link); link.click(); link.remove();
    }
    if (a === 'reset') {
      var p = 'tebaa:' + b.getAttribute('data-prefix');
      if (!b.dataset.confirm) { b.dataset.confirm = '1'; b.textContent = 'Confirmer l’effacement'; return; }
      store.keys().forEach(function (k) { if (k && k.indexOf(p) === 0) store.del(k.slice(6)); });
      location.reload();
    }
  });
})();
