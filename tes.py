from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def tugas_terjadwal(tanggal1t, tanggal1m, tanggal1d, tanggal2t, tanggal2m, tanggal2d):
    print("Cron job dijalankan dengan tanggal dari jadwal:", tanggal1t,
          tanggal1m, tanggal1d, tanggal2t, tanggal2m, tanggal2d)


def jalankan_cron():
    scheduler = BlockingScheduler()

    def ambil_tanggal_sekarang():
        return datetime.datetime.now().date()

    scheduler.add_job(tugas_terjadwal, 'cron', args=[ambil_tanggal_sekarang(
    ).year, ambil_tanggal_sekarang().month, ambil_tanggal_sekarang().day, ambil_tanggal_sekarang(
    ).year, ambil_tanggal_sekarang().month, ambil_tanggal_sekarang().day], hour=00, minute=29)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass


jalankan_cron()
