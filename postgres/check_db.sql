-- postgres/check_db.sql

-- 1) ROW COUNTS
SELECT 'estados'               AS tabela, COUNT(*) AS linhas FROM public.estados
UNION ALL
SELECT 'municipios',                    COUNT(*)       FROM public.municipios
UNION ALL
SELECT 'educacao_basica',               COUNT(*)       FROM public.educacao_basica
UNION ALL
SELECT 'infraestrutura_basica',         COUNT(*)       FROM public.infraestrutura_basica
UNION ALL
SELECT 'educacao_tecnica',              COUNT(*)       FROM public.educacao_tecnica
ORDER BY 1;


-- 2) CARDINALITY vs. MUNICÍPIOS (1:1)
SELECT
  (SELECT COUNT(*) FROM public.municipios)            AS total_municipios,
  (SELECT COUNT(*) FROM public.educacao_basica)       AS total_educacao_basica,
  (SELECT COUNT(*) FROM public.infraestrutura_basica) AS total_infra_basica
;


-- 3) MUNICÍPIOS FALTANTES nas tabelas 1:1
SELECT 'faltando_em_educacao_basica'       AS issue, m.codigo_ibge
FROM public.municipios m
LEFT JOIN public.educacao_basica e ON e.codigo_ibge = m.codigo_ibge
WHERE e.codigo_ibge IS NULL
UNION ALL
SELECT 'faltando_em_infraestrutura_basica', m.codigo_ibge
FROM public.municipios m
LEFT JOIN public.infraestrutura_basica i ON i.codigo_ibge = m.codigo_ibge
WHERE i.codigo_ibge IS NULL
ORDER BY 2;


-- 4) ORFÃOS (FK quebrada) nas 1:1
SELECT 'orfaos_educacao_basica'       AS issue, e.codigo_ibge
FROM public.educacao_basica e
LEFT JOIN public.municipios m ON m.codigo_ibge = e.codigo_ibge
WHERE m.codigo_ibge IS NULL
UNION ALL
SELECT 'orfaos_infraestrutura_basica', i.codigo_ibge
FROM public.infraestrutura_basica i
LEFT JOIN public.municipios m ON m.codigo_ibge = i.codigo_ibge
WHERE m.codigo_ibge IS NULL
ORDER BY 2;


-- 5) DUPLICATAS DE PK em educacao_tecnica (deve ser 0)
SELECT 'educacao_tecnica' AS tabela, codigo_ibge, ano_censo, COUNT(*) AS repeticoes
FROM public.educacao_tecnica
GROUP BY codigo_ibge, ano_censo
HAVING COUNT(*) > 1
;


-- 6) VALORES NEGATIVOS EM MÉTRICAS (devem ser >= 0)
WITH basics AS (
  SELECT
    'educacao_basica' AS tabela,
    unnest(ARRAY[
      matriculas_educacao_infantil, matriculas_ensino_fundamental,
      matriculas_ensino_medio, matriculas_eja,
      matriculas_educacao_especial, matriculas_ensino_tecnico,
      turmas_educacao_infantil, turmas_ensino_fundamental,
      turmas_ensino_medio, turmas_eja,
      turmas_educacao_especial, turmas_ensino_tecnico,
      docentes_educacao_infantil, docentes_ensino_fundamental,
      docentes_ensino_medio, docentes_eja,
      docentes_educacao_especial, docentes_ensino_tecnico,
      escolas_educacao_infantil, escolas_ensino_fundamental,
      escolas_ensino_medio, escolas_eja,
      escolas_educacao_especial, escolas_ensino_tecnico
    ]) AS val,
    unnest(ARRAY[
      'matriculas_educacao_infantil','matriculas_ensino_fundamental',
      'matriculas_ensino_medio','matriculas_eja',
      'matriculas_educacao_especial','matriculas_ensino_tecnico',
      'turmas_educacao_infantil','turmas_ensino_fundamental',
      'turmas_ensino_medio','turmas_eja',
      'turmas_educacao_especial','turmas_ensino_tecnico',
      'docentes_educacao_infantil','docentes_ensino_fundamental',
      'docentes_ensino_medio','docentes_eja',
      'docentes_educacao_especial','docentes_ensino_tecnico',
      'escolas_educacao_infantil','escolas_ensino_fundamental',
      'escolas_ensino_medio','escolas_eja',
      'escolas_educacao_especial','escolas_ensino_tecnico'
    ]) AS col
  FROM public.educacao_basica
  UNION ALL
  SELECT
    'infraestrutura_basica',
    unnest(ARRAY[
      escolas_com_biblioteca, escolas_com_laboratorio_ciencias,
      escolas_com_laboratorio_informatica, escolas_com_cozinha,
      escolas_com_refeitorio, escolas_com_quadra_esportes,
      escolas_com_acesso_internet, escolas_com_acessibilidade_rampas,
      profissionais_com_formacao_pedagogia, profissionais_coordenadores,
      profissionais_monitores
    ]),
    unnest(ARRAY[
      'escolas_com_biblioteca','escolas_com_laboratorio_ciencias',
      'escolas_com_laboratorio_informatica','escolas_com_cozinha',
      'escolas_com_refeitorio','escolas_com_quadra_esportes',
      'escolas_com_acesso_internet','escolas_com_acessibilidade_rampas',
      'profissionais_com_formacao_pedagogia','profissionais_coordenadores',
      'profissionais_monitores'
    ])
  FROM public.infraestrutura_basica
)
SELECT tabela, col, COUNT(*) AS negativos
FROM basics
WHERE val < 0
GROUP BY tabela, col
HAVING COUNT(*) > 0
UNION ALL
-- 6b) educacao_tecnica
SELECT
  'educacao_tecnica' AS tabela,
  col,
  COUNT(*) AS negativos
FROM (
  SELECT *,
    unnest(ARRAY[
      qt_curso_tec, qt_mat_curso_tec,
      cursos_integrados_ct, matriculas_integrados_ct,
      cursos_nivel_medio_nm, matriculas_nivel_medio_nm,
      cursos_concomitantes, matriculas_concomitantes,
      cursos_subsequentes, matriculas_subsequentes,
      cursos_eja, matriculas_eja
    ]) AS val,
    unnest(ARRAY[
      'qt_curso_tec','qt_mat_curso_tec',
      'cursos_integrados_ct','matriculas_integrados_ct',
      'cursos_nivel_medio_nm','matriculas_nivel_medio_nm',
      'cursos_concomitantes','matriculas_concomitantes',
      'cursos_subsequentes','matriculas_subsequentes',
      'cursos_eja','matriculas_eja'
    ]) AS col
  FROM public.educacao_tecnica
) t
WHERE val < 0
GROUP BY col
HAVING COUNT(*) > 0
ORDER BY tabela, col
;


-- 7) COLUNAS ESPERADAS × REAIS (faltantes/extras)
WITH expected(table_name, column_name) AS (
  VALUES
    -- estados
    ('estados','sigla'),('estados','nome'),
    -- municipios
    ('municipios','codigo_ibge'),('municipios','sigla_estado'),
    ('municipios','cidade'),('municipios','populacao_total'),
    ('municipios','ano_populacao'),('municipios','pib_per_capita'),
    ('municipios','ano_pib'),
    -- educacao_basica
    ('educacao_basica','codigo_ibge'),('educacao_basica','ano_dados'),
    ('educacao_basica','matriculas_educacao_infantil'),
    ('educacao_basica','matriculas_ensino_fundamental'),
    ('educacao_basica','matriculas_ensino_medio'),
    ('educacao_basica','matriculas_eja'),
    ('educacao_basica','matriculas_educacao_especial'),
    ('educacao_basica','matriculas_ensino_tecnico'),
    ('educacao_basica','turmas_educacao_infantil'),
    ('educacao_basica','turmas_ensino_fundamental'),
    ('educacao_basica','turmas_ensino_medio'),
    ('educacao_basica','turmas_eja'),
    ('educacao_basica','turmas_educacao_especial'),
    ('educacao_basica','turmas_ensino_tecnico'),
    ('educacao_basica','docentes_educacao_infantil'),
    ('educacao_basica','docentes_ensino_fundamental'),
    ('educacao_basica','docentes_ensino_medio'),
    ('educacao_basica','docentes_eja'),
    ('educacao_basica','docentes_educacao_especial'),
    ('educacao_basica','docentes_ensino_tecnico'),
    ('educacao_basica','escolas_educacao_infantil'),
    ('educacao_basica','escolas_ensino_fundamental'),
    ('educacao_basica','escolas_ensino_medio'),
    ('educacao_basica','escolas_eja'),
    ('educacao_basica','escolas_educacao_especial'),
    ('educacao_basica','escolas_ensino_tecnico'),
    -- infraestrutura_basica
    ('infraestrutura_basica','codigo_ibge'),
    ('infraestrutura_basica','escolas_com_biblioteca'),
    ('infraestrutura_basica','escolas_com_laboratorio_ciencias'),
    ('infraestrutura_basica','escolas_com_laboratorio_informatica'),
    ('infraestrutura_basica','escolas_com_cozinha'),
    ('infraestrutura_basica','escolas_com_refeitorio'),
    ('infraestrutura_basica','escolas_com_quadra_esportes'),
    ('infraestrutura_basica','escolas_com_acesso_internet'),
    ('infraestrutura_basica','escolas_com_acessibilidade_rampas'),
    ('infraestrutura_basica','profissionais_com_formacao_pedagogia'),
    ('infraestrutura_basica','profissionais_coordenadores'),
    ('infraestrutura_basica','profissionais_monitores'),
    -- educacao_tecnica
    ('educacao_tecnica','id'),('educacao_tecnica','codigo_ibge'),
    ('educacao_tecnica','ano_censo'),
    ('educacao_tecnica','qt_curso_tec'),('educacao_tecnica','qt_mat_curso_tec'),
    ('educacao_tecnica','cursos_integrados_ct'),
    ('educacao_tecnica','matriculas_integrados_ct'),
    ('educacao_tecnica','cursos_nivel_medio_nm'),
    ('educacao_tecnica','matriculas_nivel_medio_nm'),
    ('educacao_tecnica','cursos_concomitantes'),
    ('educacao_tecnica','matriculas_concomitantes'),
    ('educacao_tecnica','cursos_subsequentes'),
    ('educacao_tecnica','matriculas_subsequentes'),
    ('educacao_tecnica','cursos_eja'),
    ('educacao_tecnica','matriculas_eja')
),
actual AS (
  SELECT table_name, column_name
  FROM information_schema.columns
  WHERE table_schema = 'public'
)
-- faltantes
SELECT 'FALTANTE' AS tipo, e.table_name, e.column_name
FROM expected e
LEFT JOIN actual a
  ON a.table_name = e.table_name
 AND a.column_name = e.column_name
WHERE a.column_name IS NULL
UNION ALL
-- extras
SELECT 'EXTRA'   AS tipo, a.table_name, a.column_name
FROM actual a
LEFT JOIN expected e
  ON e.table_name = a.table_name
 AND e.column_name = a.column_name
WHERE e.column_name IS NULL
ORDER BY 2,3;


-- 8) CONTAGEM DE NULLs em todas as colunas
DO $$
DECLARE
  tbl TEXT;
  col TEXT;
  cnt BIGINT;
BEGIN
  RAISE NOTICE '--- CONTAGEM DE NULLs POR TABELA/COLUNA ---';
  FOR tbl IN
    SELECT unnest(ARRAY[
      'estados','municipios','educacao_basica',
      'infraestrutura_basica','educacao_tecnica'
    ])
  LOOP
    RAISE NOTICE 'Tabela: %', tbl;
    FOR col IN
      SELECT column_name
      FROM information_schema.columns
      WHERE table_schema='public' AND table_name=tbl
    LOOP
      EXECUTE format('SELECT count(*) FROM public.%I WHERE %I IS NULL', tbl, col)
      INTO cnt;
      RAISE NOTICE '  % - %: NULLs = %', tbl, col, cnt;
    END LOOP;
  END LOOP;
END
$$;
