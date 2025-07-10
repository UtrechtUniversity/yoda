let downloadZip
const downloadButton = document.getElementById('downloadZip')
try {
  downloadZip = (await import('../../static/lib/client-zip-2.5.0.js')).downloadZip
  downloadButton.classList.remove('invisible')
} catch (error) {
  console.error('Download zip import failed:', error)
}

const openAccessLink = document.getElementById('viewContents').href
const randomId = document.getElementById('viewContents').getAttribute('data-random-id')

document.body.addEventListener('click', async function (event) {
  if (event.target.matches('a#downloadZip')) {
    event.preventDefault()
    downloadButton.classList.add('disabled')
    downloadButton.innerText = 'Downloading...'

    const manifestUrl = `./${randomId}-manifest.json`
    try {
      const response = await fetch(manifestUrl)
      if (!response.ok) throw new Error(`Error: ${response.status}`)
      const entries = await response.json()

      const downloadEntries = entries.map(entry => ({
        url: `${openAccessLink}/${entry.name}`,
        name: entry.name
      }))

      if (downloadEntries.length) {
        await downloadEntriesAsZip(downloadEntries)
        console.log('ZIP download triggered.')
      }
    } catch (error) {
      console.error('ZIP failed:', error)
    } finally {
      downloadButton.innerText = 'Download as zip'
      downloadButton.classList.remove('disabled')
    }
  }
})

async function downloadEntriesAsZip (entries) {
  const zipEntries = await Promise.all(
    entries.map(async ({ url, name }) => {
      if (!url) return { name }

      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`Failed to fetch ${url}: ${response.status} ${response.statusText}`)
      }

      return { name, lastModified: Date.now(), input: response }
    })
  )

  const zipBlob = await downloadZip(zipEntries).blob()
  const downloadLink = document.createElement('a')
  downloadLink.href = URL.createObjectURL(zipBlob)
  downloadLink.download = 'download.zip'

  document.body.appendChild(downloadLink)
  downloadLink.click()
  document.body.removeChild(downloadLink)
  URL.revokeObjectURL(downloadLink.href)
}
