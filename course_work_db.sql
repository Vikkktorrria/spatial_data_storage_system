PGDMP             
        	    {            course_work_db    14.4    14.4      ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            @           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            A           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            B           1262    25015    course_work_db    DATABASE     k   CREATE DATABASE course_work_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE course_work_db;
                postgres    false            C           0    0    course_work_db    DATABASE PROPERTIES     P   ALTER DATABASE course_work_db SET search_path TO '$user', 'public', 'topology';
                     postgres    false                        2615    26091    topology    SCHEMA        CREATE SCHEMA topology;
    DROP SCHEMA topology;
                postgres    false            D           0    0    SCHEMA topology    COMMENT     9   COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';
                   postgres    false    6                        3079    25016    postgis 	   EXTENSION     ;   CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
    DROP EXTENSION postgis;
                   false            E           0    0    EXTENSION postgis    COMMENT     ^   COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';
                        false    2                        3079    26092    postgis_topology 	   EXTENSION     F   CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;
 !   DROP EXTENSION postgis_topology;
                   false    6    2            F           0    0    EXTENSION postgis_topology    COMMENT     Y   COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';
                        false    3            �            1259    26266    geometry_object    TABLE     q   CREATE TABLE public.geometry_object (
    id integer NOT NULL,
    data public.geometry,
    layer_id integer
);
 #   DROP TABLE public.geometry_object;
       public         heap    postgres    false    2    2    2    2    2    2    2    2            �            1259    26265    geometry_object_id_seq    SEQUENCE     �   ALTER TABLE public.geometry_object ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.geometry_object_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    224            �            1259    26282    layer    TABLE     F   CREATE TABLE public.layer (
    id integer NOT NULL,
    name text
);
    DROP TABLE public.layer;
       public         heap    postgres    false            �            1259    26281    layer_id_seq    SEQUENCE     �   ALTER TABLE public.layer ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.layer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    226            �            1259    26289    layers_style    TABLE     K   CREATE TABLE public.layers_style (
    layer_id integer,
    color text
);
     DROP TABLE public.layers_style;
       public         heap    postgres    false            �            1259    26314    objects_style    TABLE     M   CREATE TABLE public.objects_style (
    object_id integer,
    color text
);
 !   DROP TABLE public.objects_style;
       public         heap    postgres    false            8          0    26266    geometry_object 
   TABLE DATA           =   COPY public.geometry_object (id, data, layer_id) FROM stdin;
    public          postgres    false    224   m       :          0    26282    layer 
   TABLE DATA           )   COPY public.layer (id, name) FROM stdin;
    public          postgres    false    226   R        ;          0    26289    layers_style 
   TABLE DATA           7   COPY public.layers_style (layer_id, color) FROM stdin;
    public          postgres    false    227   �        <          0    26314    objects_style 
   TABLE DATA           9   COPY public.objects_style (object_id, color) FROM stdin;
    public          postgres    false    228   �        �          0    25333    spatial_ref_sys 
   TABLE DATA           X   COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
    public          postgres    false    213   !       �          0    26094    topology 
   TABLE DATA           G   COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
    topology          postgres    false    218   7!       �          0    26106    layer 
   TABLE DATA           �   COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
    topology          postgres    false    219   T!       G           0    0    geometry_object_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.geometry_object_id_seq', 9, true);
          public          postgres    false    223            H           0    0    layer_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.layer_id_seq', 10, true);
          public          postgres    false    225            I           0    0    topology_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);
          topology          postgres    false    217            �           2606    26272 $   geometry_object geometry_object_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.geometry_object
    ADD CONSTRAINT geometry_object_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.geometry_object DROP CONSTRAINT geometry_object_pkey;
       public            postgres    false    224            �           2606    26288    layer layer_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.layer
    ADD CONSTRAINT layer_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.layer DROP CONSTRAINT layer_pkey;
       public            postgres    false    226            �           2606    26299    layers_style laeyr_style    FK CONSTRAINT     �   ALTER TABLE ONLY public.layers_style
    ADD CONSTRAINT laeyr_style FOREIGN KEY (layer_id) REFERENCES public.layer(id) ON DELETE CASCADE NOT VALID;
 B   ALTER TABLE ONLY public.layers_style DROP CONSTRAINT laeyr_style;
       public          postgres    false    227    226    4259            �           2606    26304    geometry_object layer_of_object    FK CONSTRAINT     �   ALTER TABLE ONLY public.geometry_object
    ADD CONSTRAINT layer_of_object FOREIGN KEY (layer_id) REFERENCES public.layer(id) ON DELETE CASCADE NOT VALID;
 I   ALTER TABLE ONLY public.geometry_object DROP CONSTRAINT layer_of_object;
       public          postgres    false    226    224    4259            �           2606    26319    objects_style object_style    FK CONSTRAINT     �   ALTER TABLE ONLY public.objects_style
    ADD CONSTRAINT object_style FOREIGN KEY (object_id) REFERENCES public.geometry_object(id) ON DELETE CASCADE;
 D   ALTER TABLE ONLY public.objects_style DROP CONSTRAINT object_style;
       public          postgres    false    224    4257    228            8   �   x��QKv� \[������9E��B��1ɋ�� =13������]�&�:��B�'4�GZE[;M@NhG7�ᆠ��&?�_N����<�K�����I� #hq}��2ʛ���ȥ�K��\j�h���zC�N]���S����sO�3|��d�F��q�6��Yi�z��"�_��M��g}�ʍ�j��3q�h9Xq�'E����g�=�� � b�[      :   g   x�3��,�M�JM����2��.-JO�qM9}��ˡ\3����ԒԢ�$�2��9�wb\��_~Y~qfRfQq6T̒3,�(��$�74 j�)M��c���� ��.�      ;      x�3�L�)M�2�L/JM������ 9�      <      x�3�,��,I����� 3      �      x������ � �      �      x������ � �      �      x������ � �     