import netCDF4 as nc
import math

def dataset_mean():
    # Charger les fichiers uwnd et vwnd
    fnu = "uwnd.2000.nc"
    fnv = "vwnd.2000.nc"
    dsu = nc.Dataset(fnu)
    dsv = nc.Dataset(fnv)

    # Lire les variables uwnd et vwmd
    uwnd = dsu.variables['uwnd']
    vwnd = dsv.variables['vwnd']

    # Calculer les moyennes à l'année de uwnd et vwnd
    uwnd_mean = uwnd[:].mean(axis=0)
    vwnd_mean = vwnd[:].mean(axis=0)

    # Déterminer les dimensions de latitude, longitude et niveau
    lat_dim = dsu.dimensions['lat'].size
    lon_dim = dsu.dimensions['lon'].size
    level_dim = dsu.dimensions['level'].size

    # Création du nouveau dataset
    new_ds = nc.Dataset('vents_moyens.nc', 'w', format='NETCDF4_CLASSIC')

    # Créer les dimensions dans le nouveau dataset
    new_ds.createDimension('lat', lat_dim)
    new_ds.createDimension('lon', lon_dim)
    new_ds.createDimension('level', level_dim)

    # Créer les variables de vents moyens
    uwnd_mean_var = new_ds.createVariable('uwnd_mean', uwnd_mean.dtype, ('level', 'lat', 'lon'))
    vwnd_mean_var = new_ds.createVariable('vwnd_mean', vwnd_mean.dtype, ('level', 'lat', 'lon'))

    # Ecrire les données dans les variables
    uwnd_mean_var[:] = uwnd_mean
    vwnd_mean_var[:] = vwnd_mean

    # Fermer les fichiers
    dsu.close()
    dsv.close()
    new_ds.close()

def findMaxWnd(lat_in, lon_in, alt_in):
    # Charger les fichiers uwnd et vwnd
    dsu = nc.Dataset('uwnd.2000.nc', 'r')
    dsv = nc.Dataset('vwnd.2000.nc', 'r')

    # Lire les variables uwnd et vwnd
    uwnd_variable = dsu.variables['uwnd']
    vwnd_variable = dsv.variables['vwnd']

    # Lire les variables de latitude et longitude
    lat = dsu.variables['lat'][:]
    lon = dsu.variables['lon'][:]
    level = dsu.variables['level'][:]

    level_alt = 1013.25*(1 - (alt_in/44307.694))**5.25530
    # Déterminer les indices correspondants à la position donnée
    lat_idx = (abs(lat - lat_in)).argmin()
    lon_idx = (abs(lon - lon_in)).argmin()
    level_idx = (abs(level - level_alt)).argmin()

    # Déterminer le maximum de vitesse de vent aux latitudes et longitudes données au sol et à 20km d'altitude
    wnd_gnd_max = math.sqrt(uwnd_variable[0, 0, lat_idx, lon_idx] ** 2 + vwnd_variable[0, 0, lat_idx, lon_idx] ** 2)
    wnd_km_max = math.sqrt(uwnd_variable[0, level_idx, lat_idx, lon_idx] ** 2 + vwnd_variable[0, level_idx, lat_idx, lon_idx] ** 2)

    for t in range(len(dsu.variables['time'][:])):
        wnd_gnd = math.sqrt(uwnd_variable[t, 0, lat_idx, lon_idx]**2 + vwnd_variable[t, 0, lat_idx, lon_idx]**2)
        wnd_km = math.sqrt(uwnd_variable[t, level_idx, lat_idx, lon_idx]**2 + vwnd_variable[t, level_idx, lat_idx, lon_idx]**2)

        if wnd_gnd>wnd_gnd_max:
            wnd_gnd_max=wnd_gnd
        if wnd_km>wnd_km_max:
            wnd_km_max = wnd_km


    # Fermer les fichiers
    dsu.close()
    dsv.close()

    # Afficher les résultats
    print("Vent maximal au niveau du sol:", wnd_gnd_max)
    print("Vent maximal à 20 km d'altitude:", wnd_km_max)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    findMaxWnd(48.7,2.24,20000)
