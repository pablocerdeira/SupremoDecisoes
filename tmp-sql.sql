-- WORDS --

-- Tabela com a totalização de palavras analisadas
create table rep_total_words
select sum(word_count) total_words
from ta_words_freq;

select * from rep_total_words;


-- Tabela com a totalização de palavras distintas encontradas
create table rep_total_words_distinct
select count(distinct word) total_words_distinct
from ta_words_freq;

select * from rep_total_words_distinct;


-- Tabela com o total de linhas da tabela ta_words_freq
create table rep_total_words_lines
select max(id) total_words_lines
from ta_words_freq;

select * from rep_total_words_lines;


-- Tabela com o total de ocorrências de cada palavra
create table rep_total_words_count
select word, sum(word_count) total
from ta_words_freq
group by word
order by sum(word_count) desc;

select * from rep_total_words_count;


-- Tabela com o total de ocorrências de cada palavra nas decisões
create table rep_total_words_count_dec
select word, count(id) total
from ta_words_freq
group by word
order by count(id) desc;

select * from rep_total_words_count_dec;


-- Tabela com o total de palavras em cada decisão
create table rep_total_words_per_dec
select id, sum(word_count) total_words
from ta_words_freq
group by id
order by sum(word_count) desc;

select * from rep_total_words_per_dec;


-- Tabela com o total de palavras distintas em cada decisão
create table rep_total_words_dist_per_dec
select id, count(word) total_words_dist
from ta_words_freq
group by id
order by count(word) desc;

select * from rep_total_words_dist_per_dec;


