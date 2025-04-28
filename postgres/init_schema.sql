-- 🔹 Tabela de Estados (UF)
CREATE TABLE public.estados (
    sigla TEXT PRIMARY KEY,
    nome  TEXT NOT NULL
);

-- 🔹 Tabela de Municípios
CREATE TABLE public.municipios (
    codigo_ibge     INTEGER PRIMARY KEY,
    sigla_estado    TEXT NOT NULL REFERENCES public.estados(sigla) ON DELETE RESTRICT,
    cidade          TEXT NOT NULL,
    populacao_total INTEGER,
    ano_populacao   INTEGER,
    pib_per_capita  INTEGER,
    ano_pib         INTEGER
);

-- 🔹 Tabela de Educação Básica Agregada (ensino normal)
CREATE TABLE public.educacao_basica (
    codigo_ibge                         INTEGER PRIMARY KEY
        REFERENCES public.municipios(codigo_ibge) ON DELETE RESTRICT,
    ano_dados                           INTEGER,

    -- Matrículas
    matriculas_educacao_infantil       INTEGER,
    matriculas_ensino_fundamental      INTEGER,
    matriculas_ensino_medio            INTEGER,
    matriculas_eja                     INTEGER,
    matriculas_educacao_especial       INTEGER,
    matriculas_ensino_tecnico          INTEGER,

    -- Turmas
    turmas_educacao_infantil           INTEGER,
    turmas_ensino_fundamental          INTEGER,
    turmas_ensino_medio                INTEGER,
    turmas_eja                         INTEGER,
    turmas_educacao_especial           INTEGER,
    turmas_ensino_tecnico              INTEGER,

    -- Docentes
    docentes_educacao_infantil          INTEGER,
    docentes_ensino_fundamental         INTEGER,
    docentes_ensino_medio               INTEGER,
    docentes_eja                        INTEGER,
    docentes_educacao_especial          INTEGER,
    docentes_ensino_tecnico             INTEGER,

    -- Escolas por etapa
    escolas_educacao_infantil          INTEGER,
    escolas_ensino_fundamental         INTEGER,
    escolas_ensino_medio               INTEGER,
    escolas_eja                        INTEGER,
    escolas_educacao_especial          INTEGER,
    escolas_ensino_tecnico             INTEGER
);

-- 🔹 Infraestrutura da Educação Básica
CREATE TABLE public.infraestrutura_basica (
    codigo_ibge                         INTEGER PRIMARY KEY
        REFERENCES public.municipios(codigo_ibge) ON DELETE RESTRICT,

    -- Infraestrutura escolar
    escolas_com_biblioteca              INTEGER,
    escolas_com_laboratorio_ciencias    INTEGER,
    escolas_com_laboratorio_informatica INTEGER,
    escolas_com_cozinha                 INTEGER,
    escolas_com_refeitorio              INTEGER,
    escolas_com_quadra_esportes         INTEGER,
    escolas_com_acesso_internet         INTEGER,
    escolas_com_acessibilidade_rampas   INTEGER,

    -- Profissionais de apoio pedagógico
    profissionais_com_formacao_pedagogia INTEGER,
    profissionais_coordenadores         INTEGER,
    profissionais_monitores             INTEGER
);

-- 🔹 Tabela de Educação Técnica Agregada (por município e ano)
CREATE TABLE public.educacao_tecnica (
    id SERIAL PRIMARY KEY,
    codigo_ibge                   INTEGER NOT NULL
        REFERENCES public.municipios(codigo_ibge) ON DELETE RESTRICT,
    ano_censo                     INTEGER NOT NULL,

    -- Agregados de cursos técnicos
    qt_curso_tec                  INTEGER,
    qt_mat_curso_tec              INTEGER,
    cursos_integrados_ct          INTEGER,
    matriculas_integrados_ct      INTEGER,
    cursos_nivel_medio_nm         INTEGER,
    matriculas_nivel_medio_nm     INTEGER,
    cursos_concomitantes          INTEGER,
    matriculas_concomitantes      INTEGER,
    cursos_subsequentes           INTEGER,
    matriculas_subsequentes       INTEGER,
    cursos_eja                    INTEGER,
    matriculas_eja                INTEGER,

    UNIQUE (codigo_ibge, ano_censo)
);
